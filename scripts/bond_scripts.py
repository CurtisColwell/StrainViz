from scripts import get_atom_coords, get_connectivity_data, load_geometry, create_key
import os, re
import copy
""" Maps the energy values from the output file onto the original geometry .xyz file by digesting 
the output files and writing .tcl scripts to by viewed in VMD
"""
def map_forces(geometry, force_output):
	#Parse file for values
	bond_forces, angle_forces, dihedral_forces = force_parse(geometry[:-4] + "/" + force_output)

	bond_atoms = []
	for line in bond_forces:
		bond_atoms.append(line[1])
	
	#Use the base geometry and unoptimized dummy geometry to create a key
	key = create_key(load_geometry(geometry), load_geometry(geometry[:-4] + "/" + os.path.splitext(force_output)[0] + ".xyz"), bond_atoms)

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
	
	bond_forces_vmd, bond_min, bond_max = vmd_norm(mapped_bond_forces)
	angle_forces_vmd, angle_min, angle_max = vmd_norm(compressed_angle_forces)
	dihedral_forces_vmd, dihedral_min, dihedral_max = vmd_norm(compressed_dihedral_forces)
	
	raw_output_writer(geometry[6:-4] + "/bond_" + os.path.splitext(force_output)[0] + ".txt", copy_bond_forces)
	vmd_writer(geometry[6:-4] + "/bond_" + os.path.splitext(force_output)[0] + ".tcl", bond_forces_vmd, geometry[6:], bond_min, bond_max, "scripts/vmd_header.tcl")
	raw_output_writer(geometry[6:-4] + "/angle_" + os.path.splitext(force_output)[0] + ".txt", copy_angle_forces)
	vmd_writer(geometry[6:-4] + "/angle_" + os.path.splitext(force_output)[0] + ".tcl", angle_forces_vmd, geometry[6:], angle_min, angle_max, "scripts/vmd_header.tcl")
	raw_output_writer(geometry[6:-4] + "/dihedral_" + os.path.splitext(force_output)[0] + ".txt", copy_dihedral_forces)
	vmd_writer(geometry[6:-4] + "/dihedral_" + os.path.splitext(force_output)[0] + ".tcl", dihedral_forces_vmd, geometry[6:], dihedral_min, dihedral_max, "scripts/vmd_header.tcl")	

	return copy_bond_forces, copy_angle_forces, copy_dihedral_forces

""" Use the format atoms, bond_forces, angle_forces, dihedral_forces = force_parse("outputfile.out") 
when calling this function. Returns lists of bond, angle, and dihedral forces.
"""
def force_parse(file):
	#Read file into python and format into list
	output_lines = open(file,'r').read().splitlines()

	#Initialize needed variables
	energy_data = [[]]
	dashed_lines = 2
		
	#Get all energy data
	x = 0
	for line in output_lines:
		if '----------------------------------------------------------------------------' in line and dashed_lines == 1:
			energy_data[x].pop(0)
			energy_data.append([])
			dashed_lines += 1
			x += 1
			continue
		if '----------------------------------------------------------------------------' in line and dashed_lines == 0:
			dashed_lines += 1
		if '     Definition                    Value    dE/dq     Step     New-Value' in line:
			dashed_lines = 0
			continue
		if dashed_lines == 1:
			energy_data[x].append(line.split())
	
	#Get energy at each step
	step_energy = []
	for line in output_lines:
		if 'Total Energy       :' in line:
			step_energy.append(float(line.split()[3]))
	
	#Get energy change at each step
	step_energy_change = []
	for index, energy in enumerate(step_energy[:-1]):
		step_energy_change.append(step_energy[index+1]-step_energy[index])

	#Check for increase in step energy
	for line in step_energy_change:
		if line > 0:
			print("Positive energy change in "+file)

	#Split into bond, angle, and dihedral energies
	bond_energies = [[]]
	angle_energies = [[]]
	dihedral_energies = [[]]
	for x, set in enumerate(energy_data):
		for line in set:
			if len(line) == 8:
				bond_energies[x].append([float(line[-3])*float(line[-2])*1.889725989,[re.sub(r"\D","",line[2]),re.sub(r"\D","",line[3])]])
			if len(line) == 9:
				angle_energies[x].append([float(line[-3])*float(line[-2])*0.01745329252,[re.sub(r"\D","",line[2]),re.sub(r"\D","",line[3]),re.sub(r"\D","",line[4])]])
			if len(line) == 10:
				dihedral_energies[x].append([float(line[-3])*float(line[-2])*0.01745329252,[re.sub(r"\D","",line[2]),re.sub(r"\D","",line[3]),re.sub(r"\D","",line[4]),re.sub(r"\D","",line[5])]])
			if len(line) == 11:
				angle_energies[x].append([float(line[-3])*float(line[-2])*0.01745329252,[re.sub(r"\D","",line[2]),re.sub(r"\D","",line[3]),re.sub(r"\D","",line[4])]])
		bond_energies.append([])
		angle_energies.append([])
		dihedral_energies.append([])
	
	bond_energies.pop()
	bond_energies.pop()
	angle_energies.pop()
	angle_energies.pop()
	dihedral_energies.pop()
	dihedral_energies.pop()
	
	#Get predicted change in energy for the step
	pred_step_energy_change = []
	for set in bond_energies:
		energy = 0
		for line in set:
			energy += line[0]
		pred_step_energy_change.append(energy)

	for x, set in enumerate(angle_energies):
		energy = 0
		for line in set:
			energy += line[0]
		pred_step_energy_change[x] += energy

	for x, set in enumerate(dihedral_energies):
		energy = 0
		for line in set:
			energy += line[0]
		pred_step_energy_change[x] += energy

	#Create scaling factor for each energy step
	scale_factor = []
	for index, energy in enumerate(step_energy_change[:len(pred_step_energy_change)]):
		if pred_step_energy_change[index] == 0:
			scale_factor.append(0)
		else:
			scale_factor.append(energy/pred_step_energy_change[index])

	#Sum across all steps
	bond_energy_total = []
	angle_energy_total = []
	dihedral_energy_total = []
	for line in bond_energies[0]:
		bond_energy_total.append([0,line[1]])
	for line in angle_energies[0]:
		angle_energy_total.append([0,line[1]])
	for line in dihedral_energies[0]:
		dihedral_energy_total.append([0,line[1]])

	for x, set in enumerate(bond_energies[:len(scale_factor)]):
		for line1 in set:
			for line2 in bond_energy_total:
				if line1[1] == line2[1]:
					line2[0] -= scale_factor[x]*line1[0]

	for x, set in enumerate(angle_energies[:len(scale_factor)]):
		for line1 in set:
			for line2 in angle_energy_total:
				if line1[1] == line2[1]:
					line2[0] -= scale_factor[x]*line1[0]
	
	for x, set in enumerate(dihedral_energies[:len(scale_factor)]):
		for line1 in set:
			for line2 in dihedral_energy_total:
				if line1[1] == line2[1]:
					line2[0] -= scale_factor[x]*line1[0]

	#Return the bond, angle, and dihedral energies as lists
	return bond_energy_total, angle_energy_total, dihedral_energy_total

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

	return new_forces

""" Use the format norm_forces = normalize(forces) when calling this function.
Returns a force matrix that is normalized between 1 and 32 for VMD colours.
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
		
	return norm_force_values, minimum, maximum

""" Use the format vmd_writer("name of output.tcl", "list of normalized forces 
and the bonds they belong to", "name of geometry.xyz")
Writes the script that you can then run in the VMD Tk Console using "source script.tcl"
"""
def vmd_writer(script_name, bond_colors, geometry_filename, min, max, header):
	script = open('output/' + script_name, "w")
	script.write("# Minimum value: %s\n# Maximum value: %s\n\n" % (min*627.509, max*627.509))
	script.write("# Load a molecule\nmol new %s\n\n" % (geometry_filename))
	with open(header) as script_header:
		for line in script_header:
			script.write(line)
	script.write("\n")
	for index, line in enumerate(bond_colors):
		script.write("mol addrep top\n")
		script.write("mol modstyle %s top bonds\n" % (index+1))
		script.write("mol modcolor %s top {colorid %s}\n" % (index+1,line[0]))
		script.write("mol modselect %s top {index %s %s}\n\n" % (index+1,int(line[1][0]),int(line[1][1])))

def raw_output_writer(script_name, forces):
	output = open('output/' + script_name, "w")
	for line in forces:
		for text in line:
			output.write(str(text) + " ")
		output.write("\n")

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
				force_list.append([force[0]/(len(force[1])-1), [bond[0],bond[1]]])
	forces_compressed = []
	for bond in bonds:
		forces_compressed.append([0, bond])
	for bond in forces_compressed:
		for x in force_list:
			if bond[1] == x[1]:
				bond[0] += x[0]
	return forces_compressed

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
	
	output_forces = copy.deepcopy(new_forces)
	raw_output_writer(geometry[:-4] + "/" + force_type + "_total.txt", output_forces)

	#Write the forces to a .tcl script
	new_forces_vmd, scale_min, scale_max = vmd_norm(new_forces)
	vmd_writer(geometry[:-4] + "/" + force_type + "_total.tcl", new_forces_vmd, geometry, scale_min, scale_max, "scripts/vmd_header.tcl")

	return output_forces
	
""" This function combines all the dummies into a single picture. Forces is a list with 
the format forces[0] = [force, [c1, c2]]"""
def combine_force_types(forces, geometry):

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
		for line in forces:
			if bond[1] == line[1]:
				bond[0] += line[0]
	
	#Write the forces to a .tcl script
	raw_output_writer(geometry[:-4] + "/total_force.txt", new_forces)
	new_forces_vmd, scale_min, scale_max = vmd_norm(new_forces)
	vmd_writer(geometry[:-4] + "/total_force.tcl", new_forces_vmd, geometry, scale_min, scale_max, "scripts/vmd_header.tcl")