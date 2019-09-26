import os
import sys
from scripts import load_geometry

# Definitions

""" This function uses the base geometry.xyz and dummy.xyz files to create a Gaussian 
input file to optimize the added protons from dummy creation
"""
def create_protonopts(base, dummy, level):
	base_geometry = load_geometry(base)
	dummy_geometry = load_geometry(dummy)
	
	input_geometry = []
	for dummy_atom in dummy_geometry:
		for base_atom in base_geometry:
			found = False
			if dummy_atom[1:4] == base_atom[1:4]:
				input_geometry.append([dummy_atom[0],dummy_atom[1],"-1",dummy_atom[2],dummy_atom[3],dummy_atom[4]])
				found = True
				break
		if found == False:
			input_geometry.append(dummy_atom)
	
	script = open(os.path.splitext(dummy)[0] + "_protonopt.inp", "w")
	script.write("%NProcShared=" + sys.argv[2] + "\n#n " + level + " opt\n\n")
	script.write(" proton optimization\n\n0 1\n")
	for atom in input_geometry:
		for x in atom[1:]:
			script.write("%s\t" % x)
		script.write("\n")
	script.write("\n")

# Execution

geometry_filename = "input/" + sys.argv[1] + ".xyz"
level = sys.argv[3]

fragments = []
for file in os.listdir(geometry_filename[:-4]):
    if file.endswith(".xyz"):
        fragments.append(geometry_filename[:-4] + "/" + file)

for file in fragments:
    create_protonopts(geometry_filename, file, level)
