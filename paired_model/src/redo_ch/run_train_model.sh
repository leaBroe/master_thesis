#!/bin/bash

#SBATCH --gres=gpu:a100:1
#SBATCH --job-name=paired_model_nsp

#--config_name 'config3.json' \

python run_mlm.py \
    --model_type 'roberta' \
    --tokenizer_name ./ProteinTokenizer \
    --train_file /ibmm_data2/oas_database/paired_lea_tmp/heavy_model/train_test_val_datasets/heavy_all_seqs_train_no_ids.txt \
    --validation_file /ibmm_data2/oas_database/paired_lea_tmp/heavy_model/train_test_val_datasets/heavy_all_seqs_val_no_ids.txt \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 16 \
    --do_train \
    --do_eval \
    --do_predict \
    --evaluation_strategy 'epoch' \
    --save_strategy 'epoch' \
    --learning_rate 5e-5 \
    --weight_decay 0.1 \
    --num_train_epochs 20 \
    --lr_scheduler_type 'linear' \
    --log_level 'info' \
    --seed 42 \
    --data_seed 42 \
    --bf16 False \
    --project_name test_paired_model_nsp_mlm \
    --load_best_model_at_end True \
    --metric_for_best_model 'loss' \
    --line_by_line \
    --greater_is_better False \
    --config_name 'config3.json' \
    --report_to 'wandb' \
    --max_seq_length 30 \
    --overwrite_output_dir \
    --output_dir ./test-mlm
