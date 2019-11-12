# Minimum value: 0.0722135379111
# Maximum value: 6.94915895785

# Load a molecule
mol new test.xyz

# Change bond radii and various resolution parameters
mol representation cpk 0.8 0.0 30 5
mol representation bonds 0.2 30

# Change the drawing method of the first graphical representation to CPK
mol modstyle 0 top cpk
axes location off
display cuedensity 0.25
# Color only H atoms white
mol modselect 0 top {name H}
# Change the color of the graphical representation 0 to white
color change rgb 0 1.00 1.00 1.00
mol modcolor 0 top {colorid 0}
# The background should be white ("blue" has the colorID 0, which we have changed to white)
color Display Background blue

# Define the other colorIDs
color change rgb   1  0.000000  1.000000  0.000000
color change rgb   2  0.062500  1.000000  0.000000
color change rgb   3  0.125000  1.000000  0.000000
color change rgb   4  0.187500  1.000000  0.000000
color change rgb   5  0.250000  1.000000  0.000000
color change rgb   6  0.312500  1.000000  0.000000
color change rgb   7  0.375000  1.000000  0.000000
color change rgb   8  0.437500  1.000000  0.000000
color change rgb   9  0.500000  1.000000  0.000000
color change rgb  10  0.562500  1.000000  0.000000
color change rgb  11  0.625000  1.000000  0.000000
color change rgb  12  0.687500  1.000000  0.000000
color change rgb  13  0.750000  1.000000  0.000000
color change rgb  14  0.812500  1.000000  0.000000
color change rgb  15  0.875000  1.000000  0.000000
color change rgb  16  0.937500  1.000000  0.000000
color change rgb  17  1.000000  0.937500  0.000000
color change rgb  18  1.000000  0.875000  0.000000
color change rgb  19  1.000000  0.812500  0.000000
color change rgb  20  1.000000  0.750000  0.000000
color change rgb  21  1.000000  0.687500  0.000000
color change rgb  22  1.000000  0.625000  0.000000
color change rgb  23  1.000000  0.562500  0.000000
color change rgb  24  1.000000  0.500000  0.000000
color change rgb  25  1.000000  0.437500  0.000000
color change rgb  26  1.000000  0.375000  0.000000
color change rgb  27  1.000000  0.312500  0.000000
color change rgb  28  1.000000  0.250000  0.000000
color change rgb  29  1.000000  0.187500  0.000000
color change rgb  30  1.000000  0.125000  0.000000
color change rgb  31  1.000000  0.062500  0.000000
color change rgb  32  1.000000  0.000000  0.000000


# Adding a representation with the appropriate colorID for each bond
mol addrep top
mol modstyle 1 top bonds
mol modcolor 1 top {colorid 6}
mol modselect 1 top {index 14 13}

mol addrep top
mol modstyle 2 top bonds
mol modcolor 2 top {colorid 11}
mol modselect 2 top {index 15 14}

mol addrep top
mol modstyle 3 top bonds
mol modcolor 3 top {colorid 32}
mol modselect 3 top {index 16 15}

mol addrep top
mol modstyle 4 top bonds
mol modcolor 4 top {colorid 14}
mol modselect 4 top {index 17 16}

mol addrep top
mol modstyle 5 top bonds
mol modcolor 5 top {colorid 7}
mol modselect 5 top {index 18 17}

mol addrep top
mol modstyle 6 top bonds
mol modcolor 6 top {colorid 11}
mol modselect 6 top {index 27 16}

mol addrep top
mol modstyle 7 top bonds
mol modcolor 7 top {colorid 6}
mol modselect 7 top {index 27 26}

mol addrep top
mol modstyle 8 top bonds
mol modcolor 8 top {colorid 13}
mol modselect 8 top {index 28 15}

mol addrep top
mol modstyle 9 top bonds
mol modcolor 9 top {colorid 6}
mol modselect 9 top {index 29 28}

mol addrep top
mol modstyle 10 top bonds
mol modcolor 10 top {colorid 1}
mol modselect 10 top {index 38 13}

mol addrep top
mol modstyle 11 top bonds
mol modcolor 11 top {colorid 2}
mol modselect 11 top {index 39 14}

mol addrep top
mol modstyle 12 top bonds
mol modcolor 12 top {colorid 3}
mol modselect 12 top {index 40 17}

mol addrep top
mol modstyle 13 top bonds
mol modcolor 13 top {colorid 1}
mol modselect 13 top {index 41 18}

mol addrep top
mol modstyle 14 top bonds
mol modcolor 14 top {colorid 1}
mol modselect 14 top {index 46 26}

mol addrep top
mol modstyle 15 top bonds
mol modcolor 15 top {colorid 2}
mol modselect 15 top {index 47 27}

mol addrep top
mol modstyle 16 top bonds
mol modcolor 16 top {colorid 3}
mol modselect 16 top {index 48 28}

mol addrep top
mol modstyle 17 top bonds
mol modcolor 17 top {colorid 1}
mol modselect 17 top {index 49 29}

