# Strain Analysis Visualization

## About

This is a tool to analyze the strain of inherently strained molecules. 
[Gaussian](http://gaussian.com/glossary/g09/) is used to calculate the 
optimized geometry and strain of the molecule. 

The strain analysis uses the optimization of destrained fragments of the 
molecule to construct a picture of the strain energy mapped onto the bonds. 

[VMD](https://www.ks.uiuc.edu/Research/vmd/) is used to visualize the 
strain. All the scripts used to do this are written in Python and Bash. 

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

![StrainViz Block Diagram](https://github.com/CurtisColwell/StrainViz/blob/master/scripts/block_diagram.png)

1. Model the strained compound in Avogadro and create a Gaussian 
input file to optimize the geometry. Use B3LYP/6-31G(d) for your functional and 
basis set.

2. Use Gaussian to create an optimized geometry output file. Open this file in 
Avogadro and save it in the input/ directory with the .xyz file extension. 
Create a directory with the same name.

3. Create fragments by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain in Avogadro and save them 
as .xyz files in the directory named after the original molecule. Make sure 
that when a piece of the molecule is removed, protons are added to the empty 
bonding sites using "Build -> Add Hydrogens" in Avogadro. For an example, see 
the input/ folder where example-molecule.xyz is [5]CPP and five fragment .xyz 
files are in the related folder.

4. Run StrainViz to run multiple Gaussian jobs on each fragment and analyze 
the results. This creates .tcl files for the bond, angle and dihedral strain 
for each fragment and the combination of the fragments.
```
bash StrainViz.bash molecule-name
```

5. In VMD, open the "Tk Console" found under "Extensions", navigate to the 
output/molecule-name/ folder, and visualize the strain using the following command 
while replacing "example.tcl" for the .tcl file you would like to visualize:
```
source example.tcl
```

