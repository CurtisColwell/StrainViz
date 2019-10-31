#!bin/bash
set -e

inputname=$(basename -- "$1")
inputname="${inputname%.*}"

cd "$(dirname "$0")"
cd input/$inputname
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
mkdir -p output/$inputname
# Calculates the strain and creates .tcl files to be visualized in VMD
python scripts/StrainViz.py $inputname > output/$inputname.txt
cp input/$inputname.xyz output/$inputname
echo "[$(date +"%Y-%m-%d %T")] StrainViz analysis finished."