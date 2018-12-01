# SPiRA

SPiRA uses the Yuna package to generate a graph network from the layer polygons
of a superconducting circuit. For the time being they have to be installed from source.

The goal of SPiRA is develop a framework for IC designers to create and verify cicuit layouts. The framework uses a parameterized methodology that allows designers to generate PCells, apply rule checking, and LVS verification. The framework allows the following, though some parts are still under active development:

* **RDD**: The newly proposed Python-based PDK schema, called Rule Deck Database. This schema allows connecting directly to Python object trees for advance data manipulation.
* **PCells**: Layout generators can be created using basic Python. The framework focusses on reducing native Python boiler-plate code to improve design efficiency.
* **DRC** (experimental): Rule checking are done by placing parameter rescritions, and connecting to a Template Cell created defined in the RDD. 
* **LVS** (experimental): A graph network can be extracted using a mesh-to-graph methodology. 

## Depenencies

On Fedora install the following:

```bash
sudo dnf install redhat-rpm-config
sudo dnf install gcc-c++
sudo dnf install python3-devel
sudo dnf install tkinter
sudo dnf install gmsh
```

On ArchLinux install the following:

```bash
sudo pacman -S tk
```

## Installation

You can install SPiRA directly from the Python package manager *pip* using.
First create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install -e .
```

## Examples

Examples of using the PCell implementation is given in [examples](https://spira.readthedocs.io/en/latest/examples.html).

## History of changes

### Version 0.0.1 (Dec 01, 2018)
* Initial release.
