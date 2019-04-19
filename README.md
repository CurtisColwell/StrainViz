# Strain Analysis Visualization

## About

This is a tool to analyze the strain of inherently strained molecules. 
[Gaussian](http://gaussian.com/glossary/g09/) is used to calculate the 
optimized geometry and strain of the molecule. 

[VMD](https://www.ks.uiuc.edu/Research/vmd/) is used to visualize the 
strain. All the scripts used to do this are written in Python. 

## Installation

Run the following command on a UNIX command line:
```
git clone https://github.com/CurtisColwell/StrainViz.git
```
Or download as a zip file from the repository homepage

## Instructions

The strain analysis uses the optimization of destrained fragments of the 
molecule to construct a picture of the strain energy mapped onto the bonds 
containing the strain.

1. Model the strained compound in Avogadro and create a Gaussian 
input file to optimize the geometry.

2. Use Gaussian to create an optimized geometry output file.

3. Open the output file in avogadro and save as molecule-name.xyz in the 
input/ directory. Create a new directory there with the same name.

4. Create fragments by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain and saving them as .xyz 
files in the directory named after the original molecule.

5. Run StrainViz using the following command
```
bash StrainViz.bash molecule-name
```
This runs multiple Gaussian jobs on each fragment and analyzes the results creating 
four .tcl files for the bond, angle and dihedral strain for each fragment and four 
files that combine the fragments into a total representation.

6. In VMD, open the "Tk Console" found under "Extensions", navigate to the 
project folder, and run the command:
```
source output/example.tcl
```
to visualize the strain.
