#!bin/bash

set -e

inputname=$(basename -- "$1")
inputname="${inputname%.*}"

sbatch --job-name=$inputname --partition=short --output="output/"$inputname".txt" --account=$GROUP_NAME "slurm_submit.srun"