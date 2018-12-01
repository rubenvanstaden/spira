Overview
========

Yuna is the software package responsible for device and via detection. 
Yuna also applies polygon algorithms to the wire layer and connects the 
different wiring layers with each other and the necessary devices. 
This is done using the Clippers polygon library and the gdspy library 
that reads and parses the GDS layout file.

Layout Rules
~~~~~~~~~~~~

1. Watch out for device-to-wire connection discontinuities.
2. A device, like ntrons or jjs, must be included as a cell if it is connected to ground. And as a different cell if it is not connected to ground.
3. All ground cells must end with `_gnd`.
4. Each cell must be centered around (0, 0).
5. Wires connected to non-ground devices must be laid to connect to edges perfectly.
