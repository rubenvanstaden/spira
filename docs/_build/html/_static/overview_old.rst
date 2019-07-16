Overview
========

**SPiRA**: A parameterized design framework using Python in conjunction 
with metaprogramming techniques to allow designers to create superconducting 
and quantum parameterized circuits, while simultaneously checking for design 
rule errors. Using this parameterized gdsii a new LVS methodology is proposed 
that follows a parameterized hierarchical approach to effectively detect layout 
primitives and devices. A mesh-to-netlist algorithm is presented that extracts 
a graph netlist from a circuit layout by first meshing the conducting polygons 
into two-dimensional triangular segments. SPiRA consists of following logical 
parts, each of which is implemented as a segregated module:

* **Layout Generator Kernel** (LGK): Layout generator framework that can bind to a PDK. This involves operations on the GDSII file format elements, such as polygons, label, cell references, etc.

* **Layout Geometry Modular** (geometry): Algorithms for layout polygon operations and physical geometry construction for 2D and 3D (experimental) modeling.

* **Layout Primitive Extractor** (LPE): Detecting layout primitives, such as vias, ports, ntrons and junctions.

* **Layout Rule Checker** (LRC): Parameterized Design Rule Checker using parameter restrictions and pattern cells.

* **Layout Netlist Extractor** (LNE): Creates a graph network from a physical layout by first meshing interconnected polygon structures.


Directory Structure
-------------------

Here we discuss the folder tree structure of your SPiRA workspace. The goal of creating a 
well defined workspace structure is to effectively manage data and source files in a 
coherent fashion. The `demo` folder is an example workspace. A workspace consists of two 
parts:

* PDKs: Folder containing all the fabrication specific data.
* Projects: Folder containing the Python source file createed using spira.

**PDKs**

The folder tree of the demo workspace for the pdks are as follows:

.. code-block:: bash

    demo
    |__ pdks
        |__ components
        |__ process
        |__ templates
    |__ projects

The *components* folder contains completed PCells that are specific to a process database 
(RDD) defined in the *process* folder. The *templates* folder contains the boolean 
operation algorithms for specific primitive and device detections.

**Projects**

This folder mainly contains composed layouts that uses a defined RDD file and components 
defined in the `pdks` folder. 

.. code-block:: bash

    demo
    |__ pdks
    |__ projects
        |__ layouts
        |__ scripts
        |__ tutorials

The *layouts* diretory contains hand-designed-layouts. The SPiRA framework can be used 
to apply physical design verifiction methods on these layouts, such as DRC and LVS checks.
The *scripts* folder largly encapsulates layout generators, while the *tutorials* folder 
contains extra data.

Each workspace is linked to a single fabrication process, but using mutliple
fabs is also possible due to the simplicity of the workspace tree. 
Technically, the workspace can have any structure given that the user compensates for 
the necessary import changes. But it is highly adviced to use this structure.



