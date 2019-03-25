# Strain Analysis Visualization

## About

This is a tool to analyze the strain of inherently strained molecules. 
[Gaussian](http://gaussian.com/glossary/g09/) is used to calculate the 
optimized geometry and strain of the molecule. 

[VMD](https://www.ks.uiuc.edu/Research/vmd/) is used to visualize the 
strain. All the scripts used to do this are written in Python. 

## Installation

After downloading this repository, no installation is necessary.

## Instructions

1. Model the strained compound in Avogadro and create a Gaussian 
input file to optimize the geometry.

2. Use Gaussian to create an optimized geometry output file.

3. Open the output file in avogadro and save as an .xyz file in the 
geometry/ directory.

4. Create dummy files by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain and saving them as .xyz 
files in the dummies/ directory.

5. Run the proton_opt.py script to create input files that will optimize 
the proton added to the dummy molecules using Gaussian.

6. Once the proton has been optimized, use Gaussian to calculate molecular 
forces using the keyword "Force Geom=ModRedundant".

7. Run the StrainViz.py script to create four .tcl files for the bond, angle 
and dihedral strain and force on all atoms for each dummy file and four files 
that combine all the dummies into a total representation.

8. In VMD, open the "Tk Console" found under "Extensions", navigate to the 
project folder, and run the command:
```
source output/example.tcl
```
to visualize the strain.
