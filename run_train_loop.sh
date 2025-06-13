#!/bin/bash

# List of directories to process (sorted alphabetically)
directories=(
"0.12_42/" "0.12_53/" "0.12_64/" "0.12_75/" "0.12_86/"
"0.14_42/" "0.14_53/" "0.14_64/" "0.14_75/" "0.14_86/"
"0.16_42/" "0.16_53/" "0.16_64/" "0.16_75/" "0.16_86/"
"0.18_42/" "0.18_53/" "0.18_64/" "0.18_75/" "0.18_86/"
"0.1_42/" "0.1_53/" "0.1_64/" "0.1_75/" "0.1_86/"
"0.2_42/" "0.2_53/" "0.2_64/" "0.2_75/" "0.2_86/"
"0.3_42/" "0.3_53/" "0.3_64/" "0.3_75/" "0.3_86/"
"0.4_42/" "0.4_53/" "0.4_64/" "0.4_75/" "0.4_86/"
"0.5_42/" "0.5_53/" "0.5_64/" "0.5_75/" "0.5_86/"
"0.6_42/" "0.6_53/" "0.6_64/" "0.6_75/" "0.6_86/"
"0.7_42/" "0.7_53/" "0.7_64/" "0.7_75/" "0.7_86/"
"0.8_42/" "0.8_53/" "0.8_64/" "0.8_75/" "0.8_86/"
"0.9_42/" "0.9_53/" "0.9_64/" "0.9_75/" "0.9_86/"
"1_42/" "1_53/" "1_64/" "1_75/" "1_86/"
)


# Loop through each directory
for dir in "${directories[@]}"; do
    # Remove trailing slash for cleaner job names
    clean_dir=${dir%/}
    
    # Create the directory if it doesn't exist
    mkdir -p $dir
    
    # Create the qsub script for this parameter combination
    cat > "job_${clean_dir}.sh" << EOF
#!/bin/bash

# Change to the job directory
cd $dir/

# Set up environment variables
TRAIN_DATA=~/MacroSimGNN/Dataset/subDataset/train_validation_data_set_${clean_dir}/train/
VAL_DATA=~/MacroSimGNN/Dataset/subDataset/train_validation_data_set_${clean_dir}/test/
SAVE_PATH=./modelhistogram_new

# Run the training script
python ~/MacroSimGNN/Model/src_onehot/main.py \\
    --epochs 1000 \\
    --batch-size 256 \\
    --histogram \\
    --save-path \$SAVE_PATH \\
    --training-graphs \$TRAIN_DATA \\
    --testing-graphs \$VAL_DATA

echo "Job completed for ${clean_dir}"
EOF

    # Submit the job to the queue
    echo "Submitting job for ${clean_dir}..."
    qsub "job_${clean_dir}.sh"



done

