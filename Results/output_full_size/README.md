
Train Model
```
python ~/MacroSimGNN/Model/src/main.py --epochs 1000 --batch-size 256 --histogram  --save-path modelhistogram_new2 --training-graphs ~/MacroSimGNN/Dataset/train_validation_data_set/train/  --testing-graphs ~/MacroSimGNN/Dataset/train_validation_data_set/test/
```

Test 
```
python  ~/MacroSimGNN/Model/src/main.py --batch-size 256 --histogram --load-path path_to_save_minimum_loss_model  --testing-graphs ~/MacroSimGNN/Dataset/test2_data_set/test/
```
