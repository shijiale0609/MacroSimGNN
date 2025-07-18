"""SimGNN class and runner."""

import glob
import torch
import random
import numpy as np
import time
from tqdm import tqdm, trange
from torch_geometric.nn import GCNConv
from layers import AttentionModule, TenorNetworkModule
from utils import process_pair, calculate_loss, calculate_normalized_ged
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import MACCSkeys
from rdkit.Chem.AtomPairs import Pairs
from rdkit.Chem import rdMolDescriptors
import json

class SimGNN(torch.nn.Module):
    """
    SimGNN: A Neural Network Approach to Fast Graph Similarity Computation
    https://arxiv.org/abs/1808.05689
    """
    def __init__(self, args, number_of_labels):
        """
        :param args: Arguments object.
        :param number_of_labels: Number of node labels.
        """
        super(SimGNN, self).__init__()
        self.args = args
        self.number_labels = number_of_labels
        print("number_labels:",self.number_labels)
        self.setup_layers()

    def calculate_bottleneck_features(self):
        """
        Deciding the shape of the bottleneck layer.
        """
        if self.args.histogram == True:
            self.feature_count = self.args.tensor_neurons + self.args.bins
            print(self.feature_count, self.args.tensor_neurons, self.args.bins)
        else:
            self.feature_count = self.args.tensor_neurons

    def setup_layers(self):
        """
        Creating the layers.
        """
        self.calculate_bottleneck_features()
        self.convolution_1 = GCNConv(self.number_labels, self.args.filters_1)
        self.convolution_2 = GCNConv(self.args.filters_1, self.args.filters_2)
        self.convolution_3 = GCNConv(self.args.filters_2, self.args.filters_3)
        self.attention = AttentionModule(self.args)
        self.tensor_network = TenorNetworkModule(self.args)
        self.fully_connected_first = torch.nn.Linear(self.feature_count,
                                                     self.args.bottle_neck_neurons)
        self.scoring_layer = torch.nn.Linear(self.args.bottle_neck_neurons, 1)

    def calculate_histogram(self, abstract_features_1, abstract_features_2):
        """
        Calculate histogram from similarity matrix.
        :param abstract_features_1: Feature matrix for graph 1.
        :param abstract_features_2: Feature matrix for graph 2.
        :return hist: Histsogram of similarity scores.
        """
        scores = torch.mm(abstract_features_1, abstract_features_2).detach()
        scores = scores.view(-1, 1)
        hist = torch.histc(scores, bins=self.args.bins)
        hist = hist/torch.sum(hist)
        hist = hist.view(1, -1)
        return hist

    def convolutional_pass(self, edge_index, features):
        """
        Making convolutional pass.
        :param edge_index: Edge indices.
        :param features: Feature matrix.
        :return features: Absstract feature matrix.
        """
        features = self.convolution_1(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_2(features, edge_index)
        features = torch.nn.functional.relu(features)
        features = torch.nn.functional.dropout(features,
                                               p=self.args.dropout,
                                               training=self.training)

        features = self.convolution_3(features, edge_index)
        return features

    def forward(self, data):
        """
        Forward pass with graphs.
        :param data: Data dictiyonary.
        :return score: Similarity score.
        """
        edge_index_1 = data["edge_index_1"]
        edge_index_2 = data["edge_index_2"]
        features_1 = data["features_1"]
        features_2 = data["features_2"]

        abstract_features_1 = self.convolutional_pass(edge_index_1, features_1)
        abstract_features_2 = self.convolutional_pass(edge_index_2, features_2)

        if self.args.histogram == True:
            hist = self.calculate_histogram(abstract_features_1,
                                            torch.t(abstract_features_2))

        pooled_features_1 = self.attention(abstract_features_1)
        pooled_features_2 = self.attention(abstract_features_2)
        scores = self.tensor_network(pooled_features_1, pooled_features_2)
        scores = torch.t(scores)

        if self.args.histogram == True:
            scores = torch.cat((scores, hist), dim=1).view(1, -1)

        scores = torch.nn.functional.relu(self.fully_connected_first(scores))
        score = torch.sigmoid(self.scoring_layer(scores))
        return score

class SimGNNTrainer(object):
    """
    SimGNN model trainer.
    """
    def __init__(self, args):
        """
        :param args: Arguments object.
        """
        self.args = args
        self.initial_label_enumeration()
        self.setup_model()

    def setup_model(self):
        """
        Creating a SimGNN.
        """
        self.model = SimGNN(self.args, self.number_of_labels)

    def initial_label_enumeration(self):
        """
        Collecting the unique node idsentifiers.
        """
        print("\nEnumerating unique labels.\n")
        self.training_graphs = glob.glob(self.args.training_graphs + "*.json")
        self.training_graphs.sort(key=lambda name: int(name[len(self.args.training_graphs):-5]))
        self.testing_graphs = glob.glob(self.args.testing_graphs + "*.json")
        self.testing_graphs.sort(key=lambda name: int(name[len(self.args.testing_graphs):-5]))
        graph_pairs = self.training_graphs + self.testing_graphs
        self.global_labels = set()
        for graph_pair in tqdm(graph_pairs):
            data = process_pair(graph_pair)
            self.global_labels = self.global_labels.union(set(data["labels_1"]))
            self.global_labels = self.global_labels.union(set(data["labels_2"]))
        self.global_labels = sorted(self.global_labels)
        self.global_labels = {val:index  for index, val in enumerate(self.global_labels)}
        self.number_of_labels = 946#len(self.global_labels)
        #with open('/afs/crc.nd.edu/user/j/jshi1/scratch365/SimGNN_update/monomers_dict_full.json','r') as json_file:
        # change path to be the absolute path of monomers_dict_full.json
        with open('/Volumes/T7/MacroSimGNN/Model/monomers_dict_full_one_hot.json','r') as json_file:
            monomers_fp_dict = json.load(json_file)
        self.monomers_fp_dict = monomers_fp_dict

    def create_batches(self):
        """
        Creating batches from the training graph list.
        :return batches: List of lists with batches.
        """
        random.shuffle(self.training_graphs)
        batches = []
        for graph in range(0, len(self.training_graphs), self.args.batch_size):
            batches.append(self.training_graphs[graph:graph+self.args.batch_size])
        return batches

    def transfer_to_torch(self, data):
        """
        Transferring the data to torch and creating a hash table.
        Including the indices, features and target.
        :param data: Data dictionary.
        :return new_data: Dictionary of Torch Tensors.
        """
        new_data = dict()
        edges_1 = data["graph_1"] + [[y, x] for x, y in data["graph_1"]]

        edges_2 = data["graph_2"] + [[y, x] for x, y in data["graph_2"]]

        edges_1 = torch.from_numpy(np.array(edges_1, dtype=np.int64).T).type(torch.long)
        edges_2 = torch.from_numpy(np.array(edges_2, dtype=np.int64).T).type(torch.long)

        features_1, features_2 = [], []

        for n in data["labels_1"]:
            features_1.append(self.monomers_fp_dict[n])

        for n in data["labels_2"]:

            features_2.append(self.monomers_fp_dict[n])

        features_1 = torch.FloatTensor(np.array(features_1))
        features_2 = torch.FloatTensor(np.array(features_2))

        new_data["edge_index_1"] = edges_1
        new_data["edge_index_2"] = edges_2

        new_data["features_1"] = features_1
        #print(features_1.shape)
        #print(features_1[0], features_1[1])
        new_data["features_2"] = features_2

        norm_ged = data["ged"]/(0.5*(len(data["labels_1"])+len(data["labels_2"])))

        new_data["target"] = torch.from_numpy(np.exp(-norm_ged).reshape(1, 1)).view(-1).float()
        return new_data

    def process_batch(self, batch):
        """
        Forward pass with a batch of data.
        :param batch: Batch of graph pair locations.
        :return loss: Loss on the batch.
        """
        self.optimizer.zero_grad()
        losses = 0
        for graph_pair in batch:
            data = process_pair(graph_pair)
            data = self.transfer_to_torch(data)
            target = data["target"]
            prediction = self.model(data)
            losses = losses + torch.nn.functional.mse_loss(data["target"].unsqueeze(1), prediction)
        losses.backward(retain_graph=True)
        self.optimizer.step()
        loss = losses.item()
        return loss

    def save_model_state(self, model_state ):
        torch.save(self.model.state_dict(), model_state)

    def fit(self):
        """
        Fitting a model.
        """
        print("\nModel training.\n")

        self.optimizer = torch.optim.Adam(self.model.parameters(),
                                          lr=self.args.learning_rate,
                                          weight_decay=self.args.weight_decay)

        epochs = trange(self.args.epochs, leave=True, desc="Epoch")
        train_loss_epochs = []
        test_loss_epochs = []
        
        for epoch in epochs:
            batches = self.create_batches()
            self.loss_sum = 0
            main_index = 0
            #train_loss = 0
            self.model.train()
            for index, batch in tqdm(enumerate(batches), total=len(batches), desc="Batches"):
                loss_score = self.process_batch(batch)
                main_index = main_index + len(batch)
                self.loss_sum = self.loss_sum + loss_score * len(batch)
                loss = self.loss_sum/main_index
                epochs.set_description("Epoch (Loss=%g)" % round(loss, 5))
                #train_loss = loss

            self.save_model_state(model_state = "model_min_loss_0")    

            #train_loss_epochs.append(self.loss_sum)
            #if self.loss_sum == min(loss_sum_epochs):
            #    self.save_model_state(model_state = "model_min_loss")
            if epoch >=500 and epoch %10==0:    
                self.model.eval()
                with torch.no_grad():
                    self.test_scores = []
                    self.test_ground_truth = []
                    #targets = []
                    #predictions = []
                    for test_graph_pair in tqdm(self.testing_graphs):
                        test_data = process_pair(test_graph_pair)
                        self.test_ground_truth.append(calculate_normalized_ged(test_data))
                        test_data = self.transfer_to_torch(test_data)
                        test_target = test_data["target"]
                        test_prediction = self.model(test_data)
                        self.test_scores.append(calculate_loss(test_prediction, test_target))

                    self.train_scores = []
                    self.train_ground_truth = []
                    
                    for train_graph_pair in tqdm(self.training_graphs):
                        train_data = process_pair(train_graph_pair)
                        self.train_ground_truth.append(calculate_normalized_ged(train_data))
                        train_data = self.transfer_to_torch(train_data)
                        train_target = train_data["target"]
                        train_prediction = self.model(train_data)
                        self.train_scores.append(calculate_loss(train_prediction, train_target))
                
                
                model_test_error = np.mean(self.test_scores)  
                test_loss_epochs.append(model_test_error)
                
                model_train_error = np.mean(self.train_scores)  
                train_loss_epochs.append(model_train_error)
                
                print("test error:", model_test_error)
                print("train error:",model_train_error)
                np.save("train_loss_sum_epochs.npy" ,np.array(train_loss_epochs))
                np.save("test_loss_sum_epochs.npy" ,np.array(test_loss_epochs))

                if  test_loss_epochs[-1] == min(test_loss_epochs):
                        self.save_model_state(model_state = "model_min_loss")

        np.save("train_loss_sum_epochs.npy" ,np.array(train_loss_epochs))
        np.save("test_loss_sum_epochs.npy" ,np.array(test_loss_epochs))



    def score(self):
        """
        Scoring on the test set.
        """
        print("\n\nModel evaluation.\n")
        self.model.eval()
        self.scores = []
        self.ground_truth = []
        targets = []
        predictions = []
        predictions_time = []

        for graph_pair in tqdm(self.testing_graphs):
            data = process_pair(graph_pair)
            self.ground_truth.append(calculate_normalized_ged(data))
            data = self.transfer_to_torch(data)
            target = data["target"]
            start = time.time()
            prediction = self.model(data)
            end = time.time()
            #print(target, prediction, end-start)
            #print("target,prediction:", self.ground_truth, target.item(), prediction[0].item())
            targets.append(target.item())
            predictions.append(prediction[0].item())
            predictions_time.append(end-start)
            self.scores.append(calculate_loss(prediction, target))
        self.print_evaluation()
        np.save("targets.npy" ,np.array(targets) )
        np.save("predictions.npy" ,np.array(predictions) )
        np.save("predictions_time.npy" ,np.array(predictions_time) )

    def print_evaluation(self):
        """
        Printing the error rates.
        """
        norm_ged_mean = np.mean(self.ground_truth)
        base_error = np.mean([(n-norm_ged_mean)**2 for n in self.ground_truth])
        model_error = np.mean(self.scores)
        print("\nBaseline error: " +str(round(base_error, 5))+".")
        print("\nModel test error: " +str(round(model_error, 5))+".")

    def save(self):
        torch.save(self.model.state_dict(), self.args.save_path)

    def load(self):
        self.model.load_state_dict(torch.load(self.args.load_path))
