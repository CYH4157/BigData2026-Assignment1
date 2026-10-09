#!/usr/bin/env bash
# usage: run_queue.sh GPU_INDEX NAME:BASELINE:rank:component[,rank:component] ...
# Runs the given experiments one after another on a single GPU (nvidia-smi index).
set -u
source ~/miniconda3/etc/profile.d/conda.sh
conda activate bigdata-a1

export CUDA_DEVICE_ORDER=PCI_BUS_ID
export CUDA_VISIBLE_DEVICES=$1
export HF_HUB_DISABLE_UPDATE_CHECK=1
shift

cd ~/BigData2026-Assignment1
mkdir -p outputs/logs
for job in "$@"; do
    IFS=: read -r name baseline specs <<< "$job"
    specs=${specs//,/ }
    nb=$(python ~/a1_tools/make_run_nb.py "$name" "$baseline" $specs) || exit 1
    echo "[$(date '+%F %T')] GPU $CUDA_VISIBLE_DEVICES start $name" | tee -a outputs/logs/queue.log
    jupyter nbconvert --to notebook --execute --inplace \
        --ExecutePreprocessor.timeout=-1 "$nb" > "outputs/logs/$name.log" 2>&1
    echo "[$(date '+%F %T')] GPU $CUDA_VISIBLE_DEVICES done  $name rc=$?" | tee -a outputs/logs/queue.log
done
