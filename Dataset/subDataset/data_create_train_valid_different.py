from sklearn.model_selection import train_test_split
import json
import os



PATH = './'

for random_number in [42, 53, 64, 75, 86]:
        file_name_title = "train_validation_data_set"

        file_name = PATH + file_name_title + ".json"

        with open(PATH + file_name,'r') as json_file:
            test_data_set_section1_sample = json.load(json_file)
            
        path_train = PATH + file_name_title + "_" + str(random_number) + "/train/"
        path_test =  PATH + file_name_title + "_" + str(random_number) + "/test/"
            
        isExist = os.path.exists(path_train) and os.path.exists(path_test) 
        
        if not isExist:

           # Create a new directory because it does not exist
            os.makedirs(path_train)
            os.makedirs(path_test) 
            print("The new directory is created!")
        
        if file_name_title == "train_validation_data_set":
            sampled_graphs_train, sampled_graphs_test = train_test_split(test_data_set_section1_sample, 
                                                                     test_size=0.2, 
                                                                     random_state=random_number)
        else:
            sampled_graphs_train = []
            sampled_graphs_test = test_data_set_section1_sample
            
        
        print("generate dataset for ", file_name)
        
        for i in range(0, len(sampled_graphs_train)):
            #print(i)
            file_name = str(i)+".json"
            
            with open(path_train + file_name,'w') as fp:
                fp.write(json.dumps(sampled_graphs_train[i]))
            
 
        for i in range(0, len(sampled_graphs_test)):
            #print(i)
            file_name = str(i)+".json"
            
            with open(path_test + file_name,'w') as fp:
                fp.write(json.dumps(sampled_graphs_test[i]))
