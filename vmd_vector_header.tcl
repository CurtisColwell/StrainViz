# Change bond radii and various resolution parameters
mol representation cpk 0.8 0.5 30 5
mol representation bonds 0.2 30

# Change the drawing method of the first graphical representation to CPK
mol modstyle 0 top cpk
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

proc vmd_draw_arrow {mol start end} { 
    # an arrow is made of a cylinder and a cone 
    set middle [vecadd $start [vecscale 0.9 [vecsub $end $start]]] 
    graphics $mol cylinder $start $middle radius 0.15 
    graphics $mol cone $middle $end radius 0.25 
} 

# Adding a representation with the appropriate colorID for each bond