# SPiRA

The goal of SPiRA is develop a framework for IC designers to create and verify circuit layouts. The framework uses a parameterized methodology that allows designers to generate PCells, apply rule checking, and LVS verification. The framework allows the following, though some parts are still under active development:

* **RDD**: The newly proposed Python-based PDK schema, called Rule Deck Database. This schema allows connecting directly to Python object trees for advance data manipulation.
* **PCells**: Layout generators can be created using basic Python. The framework focusses on reducing native Python boiler-plate code to improve design efficiency.
* **DRC** (experimental): Rule checking are done by placing parameter descriptions, and connecting to a Template Cell created defined in the RDD. 
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

Documentation for other Linux systems can be found in [installation](https://spira.readthedocs.io/en/latest/installation.html)

## Installation

You can install SPiRA directly from the Python package manager *pip* using.
First create a virtual environment:

```bash
python3 -m venv env
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Normal install
pip install .

# Developer install
pip install -e .
```

## Documentation

The complete framework [documentation](https://spira.readthedocs.io/en/latest/overview.html) explains the basics of the RDD and PCell API. Note that the DRC and LVS modules are still being developed.
Examples of using the PCell implementation is given in [examples](https://github.com/rubenvanstaden/spira/tree/master/demo).
<!-- Examples of using the PCell implementation is given in [examples](https://spira.readthedocs.io/en/latest/pcell_examples.html). -->


## History of changes

### Version 0.0.2 (Jan 11, 2019)
* Implemented Manhattan routing between terminals.
* Integrated circleci.
* Started adding unit tests using pytest.
* Updated auto doc generation for classes.
* Added MidPointField for port and terminal midpoints.
* Introduces the Shape class that allows for complex point manipulations.
* Introduces `term` which is a vertical connection port.
* Routes are defined as a Shape with two connected terminal ports.

### Version 0.0.1 (Dec 01, 2018)
* Initial release.
