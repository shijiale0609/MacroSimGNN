# 1. MacroSimGNN Modification from SimGNN
To develop MacroSimGNN, we refer to and modify the source code from [SimGNN](https://github.com/benedekrozemberczki/SimGNN) to process macromolecule coarse-grained graph representations. The detailed modifications are described below.

## 1.1 Change from one-hot encoding to Morgan Fingerprint encoding.
[monomers_dict_full.json](./monomers_dict_full.json) contains the fingerprint for each monomer symbol.

load the Morgan fingerprint by setting path of monomers_dict_full.json
line 164 in [./src/simgnn.py](./src/simgnn.py)
```
        with open('path/monomers_dict_full.json','r') as json_file:
```
change path to be the absolute path of monomers_dict_full.json

## 1.2 Add validation steps to save the model that has the minimum loss on the validation dataset.

in [./src/simgnn.py](./src/simgnn.py)
```
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

            if  test_loss_epochs[-1] == min(test_loss_epochs):
                    self.save_model_state(model_state = "model_min_loss")
```

## 1.3 Add Restart command to help the model load the pre-trained model and restart.
in [./src/main.py](./src/main.py)
```
    if args.load_path and args.restart:
        trainer.load()
        trainer.fit()
```



# 2. Model Training and Testing

## 2.1 Training Command
```
TRAIN_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/train/
VAL_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/test/
SAVE_PATH=~/MacroSimGNN/Results/output_full_size/modelhistogram_new2

python ~/MacroSimGNN/Model/src/main.py \
    --epochs 1000 \
    --batch-size 256 \
    --histogram \
    --save-path $SAVE_PATH \
    --training-graphs $TRAIN_DATA \
    --testing-graphs $VAL_DATA

```

restart version
```
TRAIN_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/train/
VAL_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/test/
MODEL_PATH=~/MacroSimGNN/Results/output_full_size/model_min_loss
SAVE_PATH=~/MacroSimGNN/Results/output_full_size/modelhistogram_new2

python ~/MacroSimGNN/Model/src/main.py \
    --epochs 1000 \
    --batch-size 256 \
    --histogram \
    --restart \
    --load-path $MODEL_PATH \
    --save-path $SAVE_PATH \
    --training-graphs $TRAIN_DATA \
    --testing-graphs $VAL_DATA

```


## 2.2 Testing Command
```
TEST_DATA=~/MacroSimGNN/Dataset/test2_data_set/test/
MODEL_PATH=~/MacroSimGNN/Results/output_full_size/model_min_loss

python ~/MacroSimGNN/Model/src/main.py \
    --batch-size 256 \
    --histogram \
    --load-path $MODEL_PATH \
    --testing-graphs $TEST_DATA

```
