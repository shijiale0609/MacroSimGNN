##Training Command
```
TRAIN_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/train/
VAL_DATA=~/MacroSimGNN/Dataset/train_validation_data_set/test/
SAVE_PATH=modelhistogram_new2

python ~/MacroSimGNN/Model/src/main.py \
    --epochs 1000 \
    --batch-size 256 \
    --histogram \
    --save-path $SAVE_PATH \
    --training-graphs $TRAIN_DATA \
    --testing-graphs $VAL_DATA

```

##Testing Command 
```
TEST_DATA=~/MacroSimGNN/Dataset/test2_data_set/test/
MODEL_PATH=model_min_loss

python ~/MacroSimGNN/Model/src/main.py \
    --batch-size 256 \
    --histogram \
    --load-path $MODEL_PATH \
    --testing-graphs $TEST_DATA

```
