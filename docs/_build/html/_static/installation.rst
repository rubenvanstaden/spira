Installation
-----------------

Environment Setup
~~~~~~~~~~~~~~~~~

Yuna package descriptions:

* `docopt <http://docopt.org>`_ Command-line interface library.
* `gdspy <https://github.com/rubenvanstaden/gdspy>`_ Library for GDS file manipulations.
* `pyclipper <https://github.com/greginvm/pyclipper>`_ Python wrapper for Angusj Clipper library.
* `termcolor <https://pypi.python.org/pypi/termcolor>`_ Package for color outputs in the terminal.

Make sure Python is installed on your system:

:: 

    sudo apt-get install python-dev
    sudo apt-get install python3-dev

Install the necessary C++ compilers:

::

    sudo apt-get update 
    sudo apt-get install --reinstall build-essential

Install TKinter which is needed by Matplotlib:

::

    sudo apt-get install python-tk # Ubuntu

Installing
~~~~~~~~~~

You can install Yuna directly from the Python package manager *pip* using:

:: 

    sudo pip install yuna

To instead install Yuna from source, clone the git repository, *cd* into it, and run:

::

    sudo pip install -r requirements.txt
    sudo pip install .

We can also install the package in development mode with a symlink, so that
changes to the source files will be immediately available to other users of the
package on your system.

::

    sudo pip install -e .

Mac OS
~~~~~~

To get the Tkinter UI working in Mac, add the following file in `~/.matplotlib`:
https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python
