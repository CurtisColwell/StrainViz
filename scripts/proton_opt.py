import os
import sys
from scripts import load_geometry

# Definitions

""" This function uses the base geometry.xyz and dummy.xyz files to create a Gaussian 
input file to optimize the added protons from dummy creation
"""
def create_protonopts(base, dummy):
	base_geometry = load_geometry(base)
	dummy_geometry = load_geometry(dummy)
	
	freeze_list = []
	for num, dummy_atom in enumerate(dummy_geometry):
		for base_atom in base_geometry:
			if dummy_atom[1:4] == base_atom[1:4]:
				freeze_list.append(num)
				break
	
	script = open(os.path.splitext(dummy)[0] + "_protonopt.inp", "w")
	script.write("! " + functional + " OPT " + basis +"\n")
	script.write("%pal\n\tnprocs " + processors + "\nend\n")
	script.write("%geom\n\tConstraints\n")
	for num in freeze_list:
		script.write("\t\t{ C " + str(num) + " C }\n")
	script.write("\tend\nend\n")
	script.write("* xyz 0 1\n")
	for atom in dummy_geometry:
		for x in atom[1:]:
			if isinstance(x, float):
				x = '%f' % x
			script.write("\t%s" % x)
		script.write("\n")
	script.write("\n*")

# Execution
geometry_filename = "input/" + sys.argv[1] + ".xyz"
processors = sys.argv[2]
functional = sys.argv[3]
basis = sys.argv[4]

fragments = []
for file in os.listdir(geometry_filename[:-4]):
    if file.endswith(".xyz"):
        fragments.append(geometry_filename[:-4] + "/" + file)

for file in fragments:
    create_protonopts(geometry_filename, file)
