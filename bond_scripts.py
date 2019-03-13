from scripts import get_atom_coords, get_connectivity_data, load_geometry, create_key
import os
import copy
""" Maps the force values from the output file onto the geom.xyz file.
"""
def map_forces(geometry, force_output):
	#Parse file for values
	atoms, bond_forces, angle_forces, dihedral_forces = force_parse("dummies/" + force_output)
	
	#Open geom.xyz and create list of atom number, type, and coordinates
	atom_list = load_geometry(geometry)
	
	bond_atoms = []
	for line in bond_forces:
		bond_atoms.append(bond_forces[1])
	
	key = create_key(atom_list, atoms, bond_atoms)
				
	mapped_bond_forces = translate_forces(bond_forces, key)
	mapped_angle_forces = translate_forces(angle_forces, key)
	mapped_dihedral_forces = translate_forces(dihedral_forces, key)
	
	copy_bond_forces = copy.deepcopy(mapped_bond_forces)
	
	#Makes a list of bonds
	bonds = []
	for line in mapped_bond_forces:
		bonds.append(line[1])
	
	compressed_angle_forces = compress_forces(bonds, mapped_angle_forces)
	compressed_dihedral_forces = compress_forces(bonds, mapped_dihedral_forces)
	
	copy_angle_forces = copy.deepcopy(compressed_angle_forces)
	copy_dihedral_forces = copy.deepcopy(compressed_dihedral_forces)
	
	bond_forces_vmd, bond_min, bond_max = vmd_bond_norm(mapped_bond_forces)
	angle_forces_vmd, angle_min, angle_max = vmd_norm(compressed_angle_forces)
	dihedral_forces_vmd, dihedral_min, dihedral_max = vmd_norm(compressed_dihedral_forces)
	
	vmd_writer("vmd_bond_script_" + os.path.splitext(force_output)[0] + ".tcl", bond_forces_vmd, geometry, bond_min, bond_max, "vmd_bond_header.tcl")
	vmd_writer("vmd_angle_script_" + os.path.splitext(force_output)[0] + ".tcl", angle_forces_vmd, geometry, angle_min, angle_max, "vmd_angle_and_dihedral_header.tcl")
	vmd_writer("vmd_dihedral_script_" + os.path.splitext(force_output)[0] + ".tcl", dihedral_forces_vmd, geometry, dihedral_min, dihedral_max, "vmd_angle_and_dihedral_header.tcl")

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
	connectivity_data = get_connectivity_data(output_lines)
	
	for index, line in enumerate(force_list):
		line.append(connectivity_data[index])
	
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
	
	#Get atom coordinates
	atom_coords = get_atom_coords(output_lines)
	
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
def vmd_bond_norm(force_values):
	norm_values = []
	for line in force_values:
		norm_values.append(line[0])

	minimum = copy.deepcopy(min(norm_values))
	maximum = copy.deepcopy(max(norm_values))

	norm_max = max(norm_values)/15
	norm_min = min(norm_values)/-15
	for i in range(len(norm_values)):
		if norm_values[i] > 0:
			norm_values[i] /= norm_max
		else:
			norm_values[i] /= norm_min
		norm_values[i] += 16
		norm_values[i] = int(norm_values[i])
		
	norm_force_values = force_values
	for i in range(len(norm_force_values)):
		norm_force_values[i][0] = norm_values[i]
		
	return norm_force_values, minimum, maximum;

""" Use the format norm_forces = normalize(forces) when calling this function.
Returns a force matrix that is normalized between 1 and 32 for VMD.
"""
def vmd_norm(force_values):
	norm_values = []
	for line in force_values:
		norm_values.append(line[0])

	minimum = copy.deepcopy(min(norm_values))
	maximum = copy.deepcopy(max(norm_values))

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
		
	return norm_force_values, minimum, maximum;

""" Use the format vmd_writer("name of output.tcl", "list of normalized forces 
and the bonds they belong to", "name of geometry.xyz")
Writes the script that you can then run in the VMD Tk Console using "source script.tcl"
"""
def vmd_writer(script_name, bond_colors, geometry_filename, min, max, header):
	script = open('output/' + script_name, "w")
	script.write("# Minimum value: %s\r# Maximum value: %s\r\r" % (min, max))
	script.write("# Load a molecule\rmol new %s\r\r" % (geometry_filename))
	with open(header) as script_header:
		for line in script_header:
			script.write(line)
	script.write("\r")
	for index, line in enumerate(bond_colors):
		script.write("mol addrep top\r")
		script.write("mol modstyle %s top bonds\r" % (index+1))
		script.write("mol modcolor %s top {colorid %s}\r" % (index+1,line[0]))
		script.write("mol modselect %s top {index %s %s}\r\r" % (index+1,int(line[1][0])-1,int(line[1][1])-1))

""" Use the format compressed_forces = compress_forces(bond list, angle or dihedral 
force list)
Because multiple bonds take part in a single angle or dihedral strain, this sums
the force contribution for each bond.
"""
def compress_forces(bonds, forces):
	force_list = []
	for bond in bonds:
		for force in forces:
			if bond[0] in force[1] and bond[1] in force[1]:
				force_list.append([abs(force[0]), [bond[0],bond[1]]])
	forces_compressed = []
	for bond in bonds:
		forces_compressed.append([0, bond])
	for bond in forces_compressed:
		for x in force_list:
			if bond[1] == x[1]:
				bond[0] += x[0]
	return forces_compressed;

""" This function combines all the dummies into a single picture. Forces is a list with 
the format forces[0] = [force, [c1, c2]]"""
def combine_dummies(forces, geometry, force_type):

	#Make a bond list
	bond_list = []
	for line in forces:
		if line[1] in bond_list:
			continue
		else:
			bond_list.append(line[1])
	
	#Now make the new force list
	new_forces = []
	for line in bond_list:
		new_forces.append([0, line])
	
	#Average the forces for each bond
	for bond in new_forces:
		x = 0
		for line in forces:
			if bond[1] == line[1]:
				bond[0] += line[0]
				x += 1
		bond[0] /= x
	
	#Write the forces to a .tcl script
	new_forces_vmd, scale_min, scale_max = vmd_norm(new_forces)
	if force_type == "bond":
		vmd_writer("vmd_" + force_type + "_script_total.tcl", new_forces_vmd, geometry, scale_min, scale_max, "vmd_bond_header.tcl")
	else:
		vmd_writer("vmd_" + force_type + "_script_total.tcl", new_forces_vmd, geometry, scale_min, scale_max, "vmd_angle_and_dihedral_header.tcl")