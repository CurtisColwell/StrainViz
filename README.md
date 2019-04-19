# Strain Analysis Visualization

## About

This is a tool to analyze the strain of inherently strained molecules. 
[Gaussian](http://gaussian.com/glossary/g09/) is used to calculate the 
optimized geometry and strain of the molecule. 

The strain analysis uses the optimization of destrained fragments of the 
molecule to construct a picture of the strain energy mapped onto the bonds 
containing the strain. 

[VMD](https://www.ks.uiuc.edu/Research/vmd/) is used to visualize the 
strain. All the scripts used to do this are written in Python. 

## Installation

Run the following command on a UNIX command line:
```
git clone https://github.com/CurtisColwell/StrainViz.git
```
Or download as a zip file from the repository homepage

## Instructions

Use the following block diagram as a reference for the instructions below. 
All manual steps are shown in green, all automated steps are shown in 
red, and all intermediate files are shown in blue. The proton optimization 
files are deleted after being used.

![StrainViz Block Diagram](https://raw.githubusercontent.com/CurtisColwell/StrainViz/master/block_diagram.png)

1. Model the strained compound in Avogadro and create a Gaussian 
input file to optimize the geometry.

2. Use Gaussian to create an optimized geometry output file and save it in 
the input/ directory. Create a directory with the same name.

3. Create fragments by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain and saving them as .xyz 
files in the directory named after the original molecule.

4. Run StrainViz using the following command
```
bash StrainViz.bash molecule-name
```
This runs multiple Gaussian jobs on each fragment and analyzes the results creating 
four .tcl files for the bond, angle and dihedral strain for each fragment and four 
files that combine the fragments into a total representation.

5. In VMD, open the "Tk Console" found under "Extensions", navigate to the 
project folder, and visualize the strain using the following command command:
```
source output/example.tcl
```