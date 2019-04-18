#!bin/bash
set -e

cd dummies
# Get a list of the dummy file names
INPUT_NAMES=()
while IFS=  read -r -d $'\0'; do
	# Remove the leading ./ and following .ext
	INPUT_NAME=${REPLY##*/}
	INPUT_NAME=${INPUT_NAME%.*}
    # Add to list
	INPUT_NAMES+=("$INPUT_NAME")
done < <(find . -type f -name "*.xyz" -print0)

cd ..
# Create _protonopt.inp files to optimize the proton in Gaussian from the dummy .xyz files
python proton_opt.py
echo "[$(date +"%Y-%m-%d %T")] Proton optimization files created."

cd dummies
fileend="_protonopt"
# Run the _protonopt.inp files in Gaussian to get _protonopt.out files
module load gaussian
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file$fileend.inp" > "$file$fileend.out"
    echo "[$(date +"%Y-%m-%d %T")] $file protons optimized."
done

cd ..
# Create .inp files to calculate the energy in Gaussian from the _protonopt.out files and 
# deletes the protonopt files
python dummy_inp.py
echo "[$(date +"%Y-%m-%d %T")] Gaussian input files created."


cd dummies
# Run the .inp files in Gaussian to get .out files
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file.inp" > "$file.out"
    echo "[$(date +"%Y-%m-%d %T")] $file Gaussian run successful."
done

cd ..
# Calculates the strain and creates .tcl files to be visualized in VMD
python StrainViz.py
echo "[$(date +"%Y-%m-%d %T")] StrainViz analysis finished."