
Train Model
```
python ../src/main.py --epochs 1000 --batch-size 256 --histogram  --save-path modelhistogram_new2 --training-graphs path_to_train_dataset  --testing-graphs path_to_validation_dataset
```

Test 
```
python path_to simgnn main.py /src/main.py --batch-size 256 --histogram --load-path path_to_save_minimum_loss_model  --testing-graphs path_to_test_dataset 
```
