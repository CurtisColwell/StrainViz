#!bin/bash

set -e

inputname=$(basename -- "$1")
inputname="${inputname%.*}"

functional="${2:-"M062X"}"
basis="${3:-"6-31G**"}"
partition="${4:-"short"}"
processors="${5:-"28"}"

sbatch --job-name=$inputname --ntasks=$processors --partition=$partition --output="output/"$inputname".txt" --account=$GROUP_NAME --export=functional=$functional,basis=$basis "slurm_submit.srun"