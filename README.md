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
input file to optimize the geometry.

2. Use Gaussian to create an optimized geometry output file. Open this file in 
Avogadro and save it in the input/ directory with the .xyz file extension. 
Create a directory with the same name.

3. Create fragments by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain in Avogadro and save them 
as .xyz files in the directory named after the original molecule. Make sure 
that when a piece of the molecule is removed, protons are added to the empty 
bonding sites by drawing them at every severed bond. For an example, see 
the input/ folder where example-molecule.xyz is [5]CPP and five fragment .xyz 
files are in the related folder.

4. Run StrainViz to run multiple Gaussian jobs on each fragment and analyze 
the results. Specify the variable "molecule-name" so that it matches the geometry 
.xyz file and fragment folder, "processors-for-Gaussian" to be the number of 
processor for the Gaussian jobs, "level-of-theory" as a string that is the level 
of theory and basis set. This script creates .tcl files for the bond, angle 
and dihedral strain for each fragment and the combination of the fragments.
```
bash StrainViz.bash molecule-name processors-for-Gaussian level-of-theory
```

5. In VMD, open the "Tk Console" found under "Extensions", navigate to the 
output/molecule-name/ folder, and visualize the strain using the following command 
while replacing "example.tcl" for the .tcl file you would like to visualize:
```
source example.tcl
```

## Colour codes

In the .tcl file used to visualize the strain, the first two lines specify the minimum 
and maximum energy present in the molecule. This value is given in kcal/mol. The most 
red bond has the maximum energy and the most green bond has the minimum energy.

## Fragment creation

If there is a mistake during the run it is usually due to an error with the way the 
fragments were made and is reflected as an error in one of the Gaussian output files. 
Use the terminal output to determine where the calculation went wrong and check the 
associated output file to troubleshoot. A final note about the fragments is that the 
coordinates of the atoms that are present in the fragment and base geometry must match 
exactly or the script will not be able to translate the energy back to the base geometry.

## Using with SLURM

These jobs can be submitted to a SLURM scheduler by creating an .srun file that runs the bash 
script.
