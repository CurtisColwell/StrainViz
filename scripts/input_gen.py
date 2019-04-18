import os

# Definitions

""" This function uses the output from the proton optimization to create a Gaussian input 
file for the strain calculation
"""
def create_input(file):
	output_lines = open(file,'r').read().splitlines()
	
	read_line = False
	
	for line in output_lines:
		if ' Rotational constants (GHZ):' in line and read_line == True:
			read_line = False
			continue
		if ' Number     Number       Type             X           Y           Z' in line:
			coordinates = []
			read_line = True
			continue
		if read_line == True:
			coordinates.append(line.split())
	
	coordinates.pop()
	coordinates.pop(0)
	
	periodic_table_text = open("scripts/periodic_table.txt",'r').read().splitlines()
	periodic_table = {}
	for element in periodic_table_text:
		periodic_table[element.split()[0]] = element.split()[1]

	script = open(file[:-14] + ".inp", "w")
	script.write("#n B3LYP/6-31G(d) opt\n\n")
	script.write(" geometry optimization\n\n0 1\n")
	for atom in coordinates:
		script.write("%s\t%s\t%s\t%s\t" % (periodic_table[atom[1]], atom[3], atom[4], atom[5]))
		script.write("\n")
	script.write("\n")
	
	os.remove(file)
	os.remove(os.path.splitext(file)[0] + ".inp")

# Execution

fragments = []
fragment_folder = "input/" + sys.argv[1]
for file in os.listdir(fragment_folder):
    if file.endswith("protonopt.out"):
        fragments.append(fragment_folder + file)

for file in fragments:
    create_input(file)