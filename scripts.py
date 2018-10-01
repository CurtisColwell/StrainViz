import os
import copy
""" Maps the force values from the output file onto the geom.xyz file.
"""
def map_forces(geometry, force_output):
	#Parse file for values
	atoms, bond_forces, angle_forces, dihedral_forces = force_parse("dummies/" + force_output)
	
	#Open geom.xym and create list of atom number, type, and coordinates
	output_file = open(geometry,'r')
	output_text = output_file.read()
	output_lines = output_text.splitlines()
	output_lines.pop(0)
	output_lines.pop(0)
	atom_list = []
	for x, line in enumerate(output_lines):
		a = line.split()
		atom_list.append([x+1, a[0], float(a[1]), float(a[2]), float(a[3])])
		
	#Create a key to correlate dummy atoms to base geometry atoms
	#First number is dummy atom, second number is base geometry atom
	key = []
	extra_atoms = []
	for line1 in atom_list:
		for line2 in atoms:
			if line1[1:] == line2[1:]:
				key.append([line2[0], line1[0]])
				
	#Find atoms in dummy, but not in base geometry
	extra_atoms = []
	for line in atoms:
		if line[0] not in [x[0] for x in key]:
			extra_atoms.append(line[0])
	
	#Find atoms attached to those extra atoms
	peripheral_atoms = []
	for line in bond_forces:
		for atom in extra_atoms:
			if str(atom) == line[1][0]:
				peripheral_atoms.append(int(line[1][1]))
			elif str(atom) == line[1][1] and int(line[1][0]) not in peripheral_atoms:
				peripheral_atoms.append(int(line[1][0]))
		
	#Trim off the atoms at the ends of the dummy
	trimmed_key = []
	for line in key:
		if line[0] not in peripheral_atoms:
			trimmed_key.append(line)
				
	mapped_bond_forces = translate_forces(bond_forces, trimmed_key)
	mapped_angle_forces = translate_forces(angle_forces, trimmed_key)
	mapped_dihedral_forces = translate_forces(dihedral_forces, trimmed_key)
	
	copy_bond_forces = copy.deepcopy(mapped_bond_forces)
	copy_angle_forces = copy.deepcopy(mapped_angle_forces)
	copy_dihedral_forces = copy.deepcopy(mapped_dihedral_forces)
	
	bond_forces_vmd = vmd_norm(mapped_bond_forces)
	angle_forces_vmd = vmd_norm(mapped_angle_forces)
	dihedral_forces_vmd = vmd_norm(mapped_dihedral_forces)
	
	vmd_writer("vmd_bond_script_" + os.path.splitext(force_output)[0] + ".tcl", bond_forces_vmd, geometry)
	vmd_writer("vmd_angle_script_" + os.path.splitext(force_output)[0] + ".tcl", angle_forces_vmd, geometry)
	vmd_writer("vmd_dihedral_script_" + os.path.splitext(force_output)[0] + ".tcl", dihedral_forces_vmd, geometry)

	return copy_bond_forces, copy_angle_forces, copy_dihedral_forces;

""" Use the format var_a, var_b, var_c = force_parse("outputfile.out") when 
calling this function. Returns lists of bond, angle, and dihedral forces.
"""
def force_parse(file):
	#Read file into python and format into list
	output_file = open(file,'r')
	output_text = output_file.read()
	output_lines = output_text.splitlines()

	#Initialize needed variables
	read_line = False
	force_data = []
	force_list = []
		
	#Get force constants
	for line in output_lines:
		if '      Item               Value     Threshold  Converged?' in line and read_line == True:
			break
		if '                              (Linear)    (Quad)   (Total)' in line:
			read_line = True
			continue
		if read_line == True:
			force_data.append(line.split())
	for line in force_data:
		force_list.append([float(line[2])])
		
	#Add connectivity data
	read_line = False
	connectivity_data = []
	
	for index, line in enumerate(output_lines):
		if 'Trust Radius' in line and read_line == True:
			break
		if '! Name  Definition              Value          Derivative Info.                !' in line:
			read_line = True
			continue
		if read_line == True:
			connectivity_data.append(line.split())
	
	for index, line in enumerate(connectivity_data[1:-1]):
		try:
			force_list[index].append(line[2].strip("RAD()").split(","))
		except:
			break
	
	#Split into bond, angle, and dihedral forces
	bond_forces = []
	angle_forces = []
	dihedral_forces = []
	for line in force_list:
		if len(line[1]) == 2:
			bond_forces.append(line)
		if len(line[1]) == 3:
			angle_forces.append(line)
		if len(line[1]) == 4:
			dihedral_forces.append(line)
	
	read_line = False
	atom_coords_raw = []
	for line in output_lines:
		if ' The following ModRedundant input section has been read:' in line and read_line == True:
			break
		if ' Symbolic Z-matrix:' in line:
			read_line = True
			continue
		if read_line == True:
			atom_coords_raw.append(line.split())
	atom_coords_raw.pop()
	atom_coords_raw.pop(0)
	
	atom_coords = []
	for x, line in enumerate(atom_coords_raw):
		atom_coords.append([x+1, line[0], float(line[1]), float(line[2]), float(line[3])])
	
	#Return the bond, angle, and dihedral forces as lists
	return atom_coords, bond_forces, angle_forces, dihedral_forces;

""" Takes the forces and translates the atom numbers to correspond to the base geometry.
"""
def translate_forces(forces, key):
	forces_raw = []
	for x, a in enumerate(forces):
		forces_raw.append([a[0], []])
		for c in a[1]:
			for b in key:
				if int(c) == b[0]:
					forces_raw[x][1].append(b[1])

	new_forces = []
	for line in forces_raw:
		if len(line[1]) == len(forces[0][1]):
			new_forces.append(line)

	return new_forces;

""" Use the format norm_forces = normalize(forces) when calling this function.
Returns a force matrix that is normalized between 1 and 32 for VMD.
"""
def vmd_norm(force_values):
	norm_values = []
	for line in force_values:
		norm_values.append(line[0])

	norm_min = min(norm_values)
	for i in range(len(norm_values)):
		norm_values[i] -= norm_min

	norm_max = max(norm_values)/31
	for i in range(len(norm_values)):
		norm_values[i] /= norm_max
		norm_values[i] += 1
		norm_values[i] = int(norm_values[i])
		
	norm_force_values = force_values
	for i in range(len(norm_force_values)):
		norm_force_values[i][0] = norm_values[i]
		
	return norm_force_values;

""" Use the format vmd_writer("name of output.tcl", "list of normalized forces 
and the bonds they belong to")
Writes the script that you can then run in the VMD Tk Console using "source script.tcl"
"""
def vmd_writer(script_name, bond_colors, geometry_filename):
	script = open('output/' + script_name, "w")
	script.write("# Load a molecule\r mol new %s\r\r" % (geometry_filename))
	with open("vmd_header.tcl") as script_header:
		for line in script_header:
			script.write(line)
	script.write("\r")
	for index, line in enumerate(bond_colors):
		script.write("mol addrep top\r")
		script.write("mol modstyle %s top bonds\r" % (index+1))
		script.write("mol modcolor %s top {colorid %s}\r" % (index+1,line[0]))
		script.write("mol modselect %s top {index %s %s}\r\r" % (index+1,int(line[1][0])-1,int(line[1][1])-1))

""" Use the formate compressed_forces = compress_forces(bond list, angle or dihedral 
force list)
Because multiple bonds take part in a single angle or dihedral strain, this sums
the force contribution for each bond.
"""
def compress_forces(bonds, forces):
	force_list = []
	for bond in bonds:
		for force in forces:
			if bond[0] in force[1] and bond[1] in force[1]:
				force_list.append([force[0], [bond[0],bond[1]]])
	forces_compressed = []
	for bond in bonds:
		forces_compressed.append([0, bond])
	for bond in forces_compressed:
		for x in force_list:
			if bond[1] == x[1]:
				bond[0] += x[0]
	return forces_compressed;