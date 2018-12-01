Overview
========

SPiRA: A parameterized design framework using
Python in conjunction with metaprogramming techniques to allow designers
to create superconducting and quantum parameterized circuits, while simul-
taneously checking for design rule errors. Using this parameterized kernel a
new LVS methodology is proposed that follows a parameterized hierarchical
approach to effectively detect layout primitives and devices. A mesh-to-netlist
algorithm is presented that extracts a graph netlist from a circuit layout by first
meshing the conducting polygons into two-dimensional triangular segments. 
SPiRA consists of following logical parts, each of which is implemented as a
segregated module:

* Layout Generator Kernel (LGK): Layout generator framework that can bind to a PDK. This involves operations on the GDSII file format elements, such as polygons, label, cell references, etc.

* Layout Geometry Modular (LGM): Algorithms for layout polygon operations and physical geometry construction for 2D and 3D (experimental) modeling.

* Layout Primitive Extractor (LPE): Detecting layout primitives, such as vias, ports, ntrons and junctions.

* Layout Rule Checker (LRC): Parameterized Design Rule Checker using parameter restrictions and pattern cells.

* Layout Netlist Extractor (LNE): Creates a graph network from a physical layout by first meshing interconnected polygon structures.