#!bin/bash

set -e

inputname=$(basename -- "$1")
inputname="${inputname%.*}"

theory="${2:-"M062X/6-31G(d)"}"
partition="${3:-"short"}"
processors="${4:-"28"}"

sbatch --job-name=$inputname --ntasks=$processors --partition=$partition --output="output/"$inputname".txt" --account=$GROUP_NAME --export=theory=$theory "slurm_submit.srun"