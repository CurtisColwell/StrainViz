from scripts import get_atom_coords, get_connectivity_data, load_geometry, create_key
import os
import copy
""" Use the format var_a, var_b = force_parse("outputfile.out") when 
calling this function. Returns a list of [atom#, [forcexyz], [coordxyz]] and a key 
to the base geometry.
"""
def atom_force_parse(geometry, file):
	#Read file into python and format into list
	output_file = open("dummies/" + file,'r')
	output_text = output_file.read()
	output_lines = output_text.splitlines()
	
	#Get atom coordinates
	atom_coords = load_geometry("dummies/" + os.path.splitext(file)[0] + ".xyz")
		
	#Get atom forces
	read_line = False
	atom_forces_raw = []
	for line in output_lines:
		if 'Cartesian Forces:  Max' in line and read_line == True:
			break
		if 'Center     Atomic                   Forces (Hartrees/Bohr)' in line:
			read_line = True
			continue
		if read_line == True:
			atom_forces_raw.append(line.split())
	atom_forces_raw.pop()
	atom_forces_raw.pop(0)
	atom_forces_raw.pop(0)
	
	atom_forces = []
	for x, line in enumerate(atom_forces_raw):
		atom_forces.append([x+1, [float(line[2]),float(line[3]),float(line[4])], atom_coords[x][2:]])
		
	#Get connectivity data for the dummy geometry
	connectivity_data = get_connectivity_data(output_lines)
	
	base_atoms = load_geometry(geometry)
	
	bond_atoms = []
	for line in connectivity_data:
		if len(line) == 2:
			bond_atoms.append([int(line[0]),int(line[1])])
	
	key = create_key(base_atoms, atom_coords, bond_atoms)
	
	#Return the bond, angle, and dihedral forces as lists
	return atom_forces, key, connectivity_data;

""" Use the format vmd_writer("name of output.tcl", "list of normalized forces, start point
and end point", "name of geometry.xyz")
Writes the script that you can then run in the VMD Tk Console using "source script.tcl"
"""
def vmd_vector_writer(script_name, vector_colors, geometry_filename, min, max):
	script = open('output/' + script_name, "w")
	script.write("# Minimum: %s\r# Maximum: %s\r\r" % (min,max))
	script.write("# Load a molecule\rmol new %s\r\r" % (geometry_filename))
	with open("headers/vmd_vector_header.tcl") as script_header:
		for line in script_header:
			script.write(line)
	script.write("\r")
	for line in vector_colors:
		script.write("graphics [molinfo top] color %s\r" % (line[0]))
		script.write("vmd_draw_arrow [molinfo top] {%s %s %s} " % (line[1][0],line[1][1],line[1][2]))
		script.write("{%s %s %s}\r\r" % (line[2][0],line[2][1],line[2][2]))
		
""" Use the format norm_arrows = normalize(arrows) when calling this function.
Returns a force matrix that is normalized between 1 and 32 for VMD.
"""
def normalize(arrows):
	norm_values = []
	for line in arrows:
		norm_values.append(line[0])

	norm_min = min(norm_values)
	for i in range(len(norm_values)):
		norm_values[i] -= norm_min

	norm_max = max(norm_values)/32
	for i in range(len(norm_values)):
		norm_values[i] /= norm_max
		norm_values[i] = int(norm_values[i])
		
	norm_arrows = arrows
	for i in range(len(norm_arrows)):
		norm_arrows[i][0] = norm_values[i]
	
	for line in norm_arrows:
		line[2][0] = line[1][0] + (line[2][0]/10)
		line[2][1] = line[1][1] + (line[2][1]/10)
		line[2][2] = line[1][2] + (line[2][2]/10)
		
	norm_max += norm_min
		
	return norm_arrows, norm_min, norm_max;
	
def map_atom_forces(geometry_filename, dummy_filename):
	atom_forces, key, connectivity_data = atom_force_parse(geometry_filename, dummy_filename)
	
	dummy_atoms = []
	for atom in [x[0] for x in atom_forces]:
		if atom not in [y[0] for y in key]:
			dummy_atoms.append(atom)
	
	nearby_atoms = []
	for atom in dummy_atoms:
		for line in connectivity_data:
			if str(atom) in line and len(line) == 4:
				for x in line:
					nearby_atoms.append(int(x))

	nearby_atoms = list(set(nearby_atoms))
	
	for atom in nearby_atoms:
		for x, line in enumerate(atom_forces):
			if atom == line[0]:
				atom_forces[x] = [0]
	
	trimmed_atom_forces = []
	for line in atom_forces:
		if len(line) > 1:
			trimmed_atom_forces.append(line)
			
	copy_atom_forces = copy.deepcopy(trimmed_atom_forces)
	
	arrows = []
	for index, line in enumerate(trimmed_atom_forces):
		arrows.append([((trimmed_atom_forces[index][1][0]**2)+(trimmed_atom_forces[index][1][1])**2+(trimmed_atom_forces[index][1][2])**2)])
		arrows[index].append(trimmed_atom_forces[index][2])
		arrows[index].append(trimmed_atom_forces[index][1])
	
	norm_arrows, arrow_min, arrow_max = normalize(arrows)
	
	vmd_vector_writer("vmd_static_force_arrows_"+dummy_filename+".tcl", norm_arrows, geometry_filename, arrow_min, arrow_max)
	
	return copy_atom_forces;
	
def combine_dummy_arrows(geometry, full_atom_forces):
	atom_coords = load_geometry(geometry)
	
	combined_atom_forces = []
	for a in atom_coords:
		force = [0,0,0]
		for b in full_atom_forces:
			if a[2] == b[2][0] and a[3] == b[2][1] and a[4] == b[2][2]:
				force[0] += b[2][0]
				force[1] += b[2][1]
				force[2] += b[2][2]
		combined_atom_forces.append([force, a[2:]])
	
	arrows = []
	for index, line in enumerate(combined_atom_forces):
		arrows.append([((combined_atom_forces[index][0][0]**2)+(combined_atom_forces[index][0][1])**2+(combined_atom_forces[index][0][2])**2)])
		arrows[index].append(combined_atom_forces[index][1])
		arrows[index].append(combined_atom_forces[index][0])
		
	norm_arrows, total_min, total_max = normalize(arrows)
	
	vmd_vector_writer("vmd_static_force_arrows_total.tcl", norm_arrows, geometry, total_min, total_max)