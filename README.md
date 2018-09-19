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
input file, example.inp, to optimize the geometry.
2. Use Gaussian to calculate the optimized geometry as an output 
file, example.out.
3. Save the cartesian coordinates as an XYZ file, example.xyz, by
opening the output file with a text editor and copying the coordinates.
4. Create dummy input files that have the strain released by opening 
the file in Avogadro, deleting apropriate atoms and creating Gaussian 
input files of these strained released geometries.
5. Use Gaussian to calculate the force on all atoms by using the 
keyword Force Geom=ModRedundant in place of Opt.
6. Use the geometry file, example.xyz, and the dummy output file to
create a representation of the strain using the Python scripts 
contained in the Jupyter notebook.
7. This script will create three .tcl files.
8. Open VMD and open the "Tk Console" found under "Extensions".
9. Run the command:
```
source example.tcl
```