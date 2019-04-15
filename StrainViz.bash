#!bin/bash
set -e
module load gaussian

cd dummies
# Get a list of the dummy file names
INPUT_NAMES=()
while IFS=  read -r -d $'\0'; do
	# Remove the leading .
	INPUT_NAME=${REPLY##*/}
	INPUT_NAME=${INPUT_NAME%.*}
	INPUT_NAMES+=("$INPUT_NAME")
done < <(find . -type f -print0)

cd ..
# Create _protonopt.inp files to optimize the proton in Gaussian from the dummy .xyz files
python proton_opt.py
echo "Proton optimization files created."


cd dummies
# Run the _protonopt.inp files in Gaussian to get _protonopt.out files
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file_protonopt.inp" > "$file_protonopt.out"
    echo "$file Gaussian run successful."
done

cd ..
# Create .inp files to calculate the energy in Gaussian from the _protonopt.out files and 
# deletes the protonopt files
python dummy_inp.py
echo "Gaussian input files created."


cd dummies
# Run the .inp files in Gaussian to get .out files
for file in "${INPUT_NAMES[@]}"; do
    g09 < "$file.inp" > "$file.out"
    echo "$file Gaussian run successful."
done

cd ..
# Calculates the strain and creates .tcl files to be visualized in VMD
python StrainViz.py
echo "StrainViz analysis finished."