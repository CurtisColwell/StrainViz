#!bin/bash
set -e

cd "$(dirname "$0")"
cd input/$1
# Get a list of the dummy file names
INPUT_NAMES=()
while IFS=  read -r -d $'\0'; do
	# Remove the leading ./ and following .ext
	INPUT_NAME=${REPLY##*/}
	INPUT_NAME=${INPUT_NAME%.*}
    # Add to list
	INPUT_NAMES+=("$INPUT_NAME")
done < <(find . -type f -name "*.xyz" -print0)

cd ../..
# Create _protonopt.inp files to optimize the proton in Gaussian from the dummy .xyz files
python scripts/proton_opt.py $1 $2 $3
echo "[$(date +"%Y-%m-%d %T")] Proton optimization files created."

cd input/$1
fileend="_protonopt"
# Run the _protonopt.inp files in Gaussian to get _protonopt.out files
module load gaussian
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file$fileend.inp" > "$file$fileend.out" || echo "[$(date +"%Y-%m-%d %T")] $file proton optimization failed."
    echo "[$(date +"%Y-%m-%d %T")] $file protons optimized."
done

cd ../..
# Create .inp files to calculate the energy in Gaussian from the _protonopt.out files and 
# deletes the protonopt files
python scripts/input_gen.py $1 $2 $3
echo "[$(date +"%Y-%m-%d %T")] Gaussian input files created."


cd input/$1
# Run the .inp files in Gaussian to get .out files
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file.inp" > "$file.out" || echo "[$(date +"%Y-%m-%d %T")] $file energy calculation failed."
    echo "[$(date +"%Y-%m-%d %T")] $file Gaussian run successful."
done

cd ../..
mkdir -p output/$1
# Calculates the strain and creates .tcl files to be visualized in VMD
python scripts/StrainViz.py $1
cp input/$1.xyz output/$1
echo "[$(date +"%Y-%m-%d %T")] StrainViz analysis finished."