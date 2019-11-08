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
# Create _protonopt.inp files to optimize the proton in Orca from the dummy .xyz files
python scripts/proton_opt.py $1 $2 $3 $4
echo "[$(date +"%Y-%m-%d %T")] Proton optimization files created."


cd input/$1
fileend="_protonopt"
# Run the _protonopt.inp files in Orca to get _protonopt.out files
module load orca
WORK_DIR=$PWD
TEMP_DIR=$(mktemp -d)
for file in "${INPUT_NAMES[@]}"; do
    cp "$file$fileend.inp" "$TEMP_DIR/"
    cd "$TEMP_DIR"
    $(command -v orca) "$file$fileend.inp" > "$file$fileend.out" || echo "[$(date +"%Y-%m-%d %T")] $file proton optimization failed."
    cp "$file$fileend.out" "$WORK_DIR/"
    echo "[$(date +"%Y-%m-%d %T")] $file proton optimization done."
    cd "$WORK_DIR"
done

cd ../..
# Create .inp files to calculate the energy in Orca from the _protonopt.out files and 
# deletes the protonopt files
python scripts/input_gen.py $1 $2 $3 $4
echo "[$(date +"%Y-%m-%d %T")] Orca input files created."

cd input/$1
# Run the .inp files in Orca to get .out files
for file in "${INPUT_NAMES[@]}"; do
    cp "$file.inp" "$TEMP_DIR/"
    cd "$TEMP_DIR"
    $(command -v orca) "$file.inp" > "$file.out" || echo "[$(date +"%Y-%m-%d %T")] $file energy calculation failed."
    cp "$file.out" "$WORK_DIR/"
    echo "[$(date +"%Y-%m-%d %T")] $file Orca run done."
    cd "$WORK_DIR"
done

rm -rf "$TEMP_DIR"

cd ../..
mkdir -p output/$1
# Calculates the strain and creates .tcl files to be visualized in VMD
python scripts/StrainViz.py $1
cp input/$1.xyz output/$1
echo "[$(date +"%Y-%m-%d %T")] StrainViz analysis finished."