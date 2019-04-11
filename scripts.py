import os
""" Get atom coordinates
"""
def get_atom_coords(output_lines):
	read_line = False
	atom_coords_raw = []
	for line in output_lines:
		if 'GradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGradGrad' in line and read_line == True:
			break
		if ' Symbolic Z-matrix:' in line:
			read_line = True
			continue
		if read_line == True:
			atom_coords_raw.append(line.split())
	atom_coords_raw.pop()
	atom_coords_raw.pop()
	atom_coords_raw.pop(0)
	
	atom_coords = []
	for x, line in enumerate(atom_coords_raw):
		atom_coords.append([x+1, line[0], float(line[1]), float(line[2]), float(line[3])])
		
	return atom_coords;
	
""" Get connectivity data
"""
def get_connectivity_data(output_lines):
	read_line = False
	raw_connectivity_data = []
	
	for index, line in enumerate(output_lines):
		if 'Trust Radius' in line and read_line == True:
			break
		if '! Name  Definition              Value          Derivative Info.                !' in line:
			read_line = True
			continue
		if read_line == True:
			raw_connectivity_data.append(line.split())
	
	connectivity_data = []
	for line in raw_connectivity_data[1:-1]:
		connectivity_data.append(line[2].strip("RAD()").split(","))
	
	return connectivity_data;

""" Load geometry atoms into list
"""
def load_geometry(geometry):
	output_file = open(geometry,'r')
	output_text = output_file.read()
	output_lines = output_text.splitlines()
	output_lines.pop(0)
	output_lines.pop(0)
	atom_list = []
	for x, line in enumerate(output_lines):
		a = line.split()
		atom_list.append([x+1, a[0], float(a[1]), float(a[2]), float(a[3])])
		
	return atom_list;

"""Create a key to correlate dummy atoms to base geometry atoms
First number is dummy atom, second number is base geometry atom
"""
def create_key(base_atoms, dummy_atoms, bond_atoms):
	key = []
	extra_atoms = []
	for line1 in base_atoms:
		for line2 in dummy_atoms:
			if line1[1:] == line2[1:]:
				key.append([line2[0], line1[0]])
				
	#Find atoms in dummy, but not in base geometry
	extra_atoms = []
	for line in dummy_atoms:
		if line[0] not in [x[0] for x in key]:
			extra_atoms.append(line[0])
	
	#Find atoms attached to those extra atoms
	peripheral_atoms = []
	for line in bond_atoms:
		for atom in extra_atoms:
			if str(atom) == line[0]:
				peripheral_atoms.append(int(line[1]))
			elif str(atom) == line[1] and int(line[0]) not in peripheral_atoms:
				peripheral_atoms.append(int(line[0]))
		
	#Trim off the atoms at the ends of the dummy
	trimmed_key = []
	for line in key:
		if line[0] not in peripheral_atoms:
			trimmed_key.append(line)
			
	return trimmed_key;
	
""" This function uses the base geometry.xyz and dummy.xyz files to create Gaussian 
input files to optimize any added or out of place atoms from dummy creation"""

def create_protonopts(base, dummy):
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
	script.write("#n B3LYP/6-31G(d) opt\n\n")
	script.write(" placeholder\n\n0 1\n")
	for atom in input_geometry:
		for x in atom[1:]:
			script.write("%s\t" % x)
		script.write("\n")
	script.write("\n")
	
def print_total(energies, type):
	energy = 0
	for line in energies:
		energy += line[0]
	print(type + " is " + str(energy*627.509) + "kcal/mol")