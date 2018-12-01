# SPiRA

SPiRA uses the Yuna package to generate a graph network from the layer polygons
of a superconducting circuit. For the time being they have to be installed from source.

## User

Setup for the normal user.

### Depenencies

On Fedora install the following:

```bash
sudo dnf install redhat-rpm-config
sudo dnf install gcc-c++
sudo dnf install python3-devel
sudo dnf install tkinter
sudo dnf install gmsh
```

### Installation

You can install SPiRA directly from the Python package manager *pip* using.
First create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install -e .
```

# Examples

To run examples, *cd* into the `/pcells/examples/stable` directory and run any script
using Python 3. The examples in the *unstable* directory is to show progress of changes
made in the software versions and should be ignored by the average user.

## Developers

Documentation for developers for maintaining and extending.
To instead install ExVerify from source, clone this repository, *cd* into it, and run:

```bash
pip install -r requirements.txt
pip install .
pip install -e .
```

Uploading package to PyPi using *twine*:

Remember to remove all Eggs before doing a push to PyPi.

```bash
sudo python3 setup.py bdist_wheel
twine upload dist/*
```

To install package systemwide set the prefix value when running setuptools:

```bash
sudo python3 setup.py install --prefix=/usr
```

or

NB dont use sudo or --user when install from sourc ein a virtual enviroment.

```bash
sudo python3 -m pip install --upgrade .
```

* https://docs.python.org/3.3/install/index.html

Unit testing overview: http://docs.python-guide.org/en/latest/writing/tests/

### Documentation

If you want to generate the docs make sure the Napoleon package is installed:

```bash
pip install sphinxcontrib-napoleon
```

Coding standards for parsing the correct docs is given in:

* https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

* https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt

Introduction to Python Virtual Enviroments:

* https://realpython.com/python-virtual-environments-a-primer/
* https://stackoverflow.com/questions/15746675/how-to-write-a-python-module-package
