import os
import sys

# Definitions

""" This function uses the output from the proton optimization to create a Gaussian input 
file for the strain calculation
"""
def create_input(file):
	output_lines = open(file,'r').read().splitlines()
	
	read_line = False
	
	for line in output_lines:
		if '(A.U.)' in line and read_line == True:
			read_line = False
			break
		if '*** FINAL ENERGY EVALUATION AT THE STATIONARY POINT ***' in line:
			coordinates = []
			read_line = True
			continue
		if read_line == True:
			coordinates.append(line)
	
	for _ in range(2):
		coordinates.pop()
	for _ in range(5):
		coordinates.pop(0)

	script = open(file[:-14] + ".inp", "w")

	script.write("! " + functional + " OPT " + basis +"\n")
	script.write("%pal\n\tnprocs " + processors + "\nend\n")
	script.write("%geom\n\tcoordsys redundant_old\nend\n")
	script.write("* xyz 0 1\n")
	for line in coordinates:
		script.write(line + "\n")
	script.write("\n*")

	os.remove(file)
	os.remove(os.path.splitext(file)[0] + ".inp")

# Execution

processors = sys.argv[2]
functional = sys.argv[3]
basis = sys.argv[4]
fragments = []
fragment_folder = "input/" + sys.argv[1] + "/"
for file in os.listdir(fragment_folder):
    if file.endswith("protonopt.out"):
        fragments.append(fragment_folder + file)

for file in fragments:
    create_input(file)