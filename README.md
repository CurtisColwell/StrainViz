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

1. Optimize the geometry using gaussian.
2. Take the output file and create an .xyz from the output 
file by copy and pasting the final atom positions.
3. Open in Avogadro and delete atoms to create dummy force 
calculation input files.
4. Do the force calculation.
5. Use the scripts.