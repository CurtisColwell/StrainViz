# Change bond radii and various resolution parameters
mol representation cpk 0.8 0.0 30 5
mol representation bonds 0.2 30

# Change the drawing method of the first graphical representation to CPK
mol modstyle 0 top cpk
# Color only H atoms white
mol modselect 0 top {name H}
# Change the color of the graphical representation 0 to white
color change rgb 0 1.00 1.00 1.00
mol modcolor 0 top {colorid 0}
# The background should be white ("blue" has the colorID 0, which we have changed to white)
color Display Background blue

# Define the other colorIDs
color change rgb 1  0     0     1
color change rgb 2  0     0.125 1
color change rgb 3  0     0.25  1
color change rgb 4  0     0.375 1
color change rgb 5  0     0.5   1
color change rgb 6  0     0.625 1
color change rgb 7  0     0.75  1
color change rgb 8  0     0.875 1
color change rgb 9  0     1     0.875
color change rgb 10 0     1     0.75
color change rgb 11 0     1     0.625
color change rgb 12 0     1     0.5
color change rgb 13 0     1     0.375
color change rgb 14 0     1     0.25
color change rgb 15 0     1     0.125
color change rgb 16 0     1     0
color change rgb 17 0.125 1     0
color change rgb 18 0.25  1     0
color change rgb 19 0.375 1     0
color change rgb 20 0.5   1     0
color change rgb 21 0.625 1     0
color change rgb 22 0.75  1     0
color change rgb 23 0.875 1     0
color change rgb 24 1     1     0
color change rgb 25 1     0.875 0
color change rgb 26 1     0.75  0
color change rgb 27 1     0.625 0
color change rgb 28 1     0.5   0 
color change rgb 29 1     0.375 0
color change rgb 30 1     0.25  0
color change rgb 31 1     0.125 0
color change rgb 32 1     0     0


# Adding a representation with the appropriate colorID for each bond