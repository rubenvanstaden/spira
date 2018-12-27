Installation
============

This page gives more information about installing and setting up the SPiRA framework. 

Environment Setup
-----------------

SPiRA package descriptions:

* `gdspy <https://github.com/rubenvanstaden/gdspy>`_ Library for GDS file manipulations.
* `pyclipper <https://github.com/greginvm/pyclipper>`_ Python wrapper for Angusj Clipper library.
* `pygmsh <https://github.com/nschloe/pygmsh>`_ The goal of pygmsh is to combine the power of Gmsh with the versatility of Python and to provide useful abstractions from the Gmsh scripting language so you can create complex geometries more easily.
* `meshio <https://github.com/nschloe/meshio>`_ A package to read and write different mesh formats.
* `NetworkX <https://networkx.github.io/>`_ A Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.

Ubuntu
------

The following packages has to be installed for Ubuntu systems.

.. code-block:: bash
    :linenos:

    sudo apt-get install python-dev
    sudo apt-get install python3-dev
    sudo apt-get install --reinstall build-essential
    sudo apt-get install python-tk # Ubuntu
    sudo apt-get update

ArchLinux
---------

On ArchLinux install the following:

.. code-block:: bash
    :linenos:

    sudo pacman -S tk

FreeBSD
-------

Support to be added in Q1 2019.


