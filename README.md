# Strain Analysis Visualization

<img src="https://github.com/CurtisColwell/StrainViz/blob/orca/scripts/figures/StrainViz.png" alt="StrainViz Logo" width="250">

## About

This is a tool to analyze the strain of inherently strained molecules. 
[Orca](https://orcaforum.kofo.mpg.de/app.php/portal) is used to calculate the 
optimized geometry and strain of the molecule. The strain analysis uses 
the optimization of destrained fragments of the molecule to construct a 
picture of the strain energy mapped onto the bonds. [VMD](https://www.ks.uiuc.edu/Research/vmd/) 
is used to visualize the strain. All the scripts used to do this are 
written in Python and Bash.

This tool was written by [Curtis Colwell](https://github.com/CurtisColwell) 
in the [Jasti Group](https://pages.uoregon.edu/jastilab/) at the University of Oregon.

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

![StrainViz Block Diagram](https://github.com/CurtisColwell/StrainViz/blob/orca/scripts/figures/block_diagram.png)

1. Model the strained compound in Avogadro and create an Orca
input file to optimize the geometry.

2. Use Orca to create an optimized geometry output file. Open this file in 
Avogadro and save it in the input/ directory with the .xyz file extension. 
Create a directory with the same name.

3. Create fragments by symmetrically deleting portions of the molecule 
that will allow the molecule to release its strain in Avogadro and save them 
as .xyz files in the directory named after the original molecule. Make sure 
that when a piece of the molecule is removed, protons are added to the empty 
bonding sites by drawing them at every severed bond. For an example, see 
the input/ folder where example-molecule.xyz is [5]CPP and five fragment .xyz 
files are in the related folder.

4. Run StrainViz to run multiple Orca jobs on each fragment and analyze 
the results. Specify the variable "molecule-name" so that it matches the geometry 
.xyz file and fragment folder, "processors" to be the number of 
processor for the Orca jobs, "functional" as a string that is the functional and 
"basis" is a string that is the basis set. This script creates .tcl files for the bond, angle 
and dihedral strain for each fragment and the combination of the fragments.
```
bash StrainViz.bash molecule-name processors functional basis
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

<img src="https://github.com/CurtisColwell/StrainViz/blob/orca/scripts/figures/example_colour_scale.png" alt="Colour Scale" width="250">

## Fragment creation

Create fragments that are relatively symmetric and do not create unconventional functional 
groups. Only two fragments are necessary to cover all bonds in the molecule and a good 
approximation of the total strain can be obtained, however, the more fragments you have, the 
more accurate the local strain map will become as long as these fragments are large and 
created symmetrically.
If there is a mistake during the run it is usually due to an error with the way the 
fragments were made and is reflected as an error in one of the Orca output files. 
Use the terminal output to determine where the calculation went wrong and check the 
associated output file to troubleshoot. A final note about the fragments is that the 
coordinates of the atoms that are present in the fragment and base geometry must match 
exactly or the script will not be able to translate the energy back to the base geometry.

## Resubmitting

If the Orca jobs have already been run and it is only needed to resubmit the calculation 
of the strain, the script Recalc.bash can be used. This script uses the input format:
```
bash Recalc.bash input/example molecule
```

## Result Quality

If the optimizations are not working ideally, there are a few flags that will appear. 

### Orca Job Failure
If an Orca job fails, a note will appear saying which input file generated the failure. This is 
the most common reason for the script to not work properly. If any job fails, the script will 
continue, but will likely error out later on due to missing information. Even if the script 
has enough information to complete the analysis, the results will likely not be correct.
### Negative Strain Energy
If negative strain energies are calculated, a flag will appear saying which output file was 
analyzed to determine negative strain energies. Negative strain energies can be a hallmark
of a failed calculation, but if they are close to zero, may be real and part of the calculation 
as long as they do not result in an overall negative strain.
### Increase in Energy During Optimization
If at any point in a fragment geometry optimization a step that increases the energy is taken, 
a flag will appear noting it. Steep increases in energy as well as trailing optimizations with 
many small increases in energy often result in bizarre results. Resubmitting these jobs with the 
keyword opt=CalcAll will result in a more computationally intensive, but cleaner trajectory.

## Using with SLURM

These jobs can be submitted to a SLURM scheduler by running slurm.bash with the name of 
the molecule to submit.
```
bash slurm.bash input/example-molecule functional basis partition processors
```
The functional defaults to "M062X", the basis to "6-31G**", the partition defaults to short, and the 
number of processors defaults to 28 if nothing is written in the command.
