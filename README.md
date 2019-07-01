# SPiRA

**SPiRA** is a parameterized design framework using Python in conjunction with metaprogramming
techniques to allow designers to create *superconducting* and *quantum* parameterized circuits,
while simultaneously checking for design violations, through a novel methodology called *validate-by-design*. 
Creating PCells and extracting a model from a layout requires data from the fabrication process. 
A new PDK scheme is introduced, called the Rule Deck Database (RDD), which effectively connects
process data to the SPiRA framework. The aim of the SPiRA framework is to:

* Create a PCell framework that is easy to use by designers with the focus falling on Superconducting Digital Electronics (SDE).
* The framework must be able to effectively connect process data to layout elements. Data parsing must be generic to be adaptable to future technology changes.

## Depenencies

On Fedora install the following:

```bash
sudo dnf install redhat-rpm-config
sudo dnf install gcc-c++
sudo dnf install python3-devel
sudo dnf install tkinter
sudo dnf install gmsh
```

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

<!-- The complete framework [documentation](https://spira.readthedocs.io/en/latest/overview.html) explains the basics of the RDD and PCell API. Note that the DRC and LVS modules are still being developed.
Examples of using the PCell implementation is given in [examples](https://github.com/rubenvanstaden/spira/tree/master/demo). -->
For more examples please contact Ruben van Staden <rubenvanstaden@gmail.com>.

## Known Issues
* There are some issues with Reflection Transformation.

## Future Changes
* Update polygon to include rounded corners.

## History of changes

### Version 0.1.0 (July 1, 2019)
* Added the documentation.
* Introduces *derived layers* to allow for layer boolean operations.
* Introduces *process* and *purpose* parameters.
* Updated the edge generation algorithms to include both an outside and inside edge.
* Updated the routing algorithms to use new ``gdspy`` features.
* Added stretching operations.
* Extended the RDD to include *display resources*.
* Fix issues with writing to a GDSII file.
* Added snap to grid functionality.
* Implemented parameters caching.
* Added sref-to-port alignment.
* Upgraded `Midpoint` class to Coord.
* Added `PortList` class for special port filtering functionality.
* Updated ``spira.Port`` to have a ``port_type`` parameter, rather than having multiple port classes.
* Renamed ``elemental`` to ``elements``, since ``spira.Cell`` does not inherit from ``gdspy.Cell`` anymore.
* Created layer mappers.
* Changed the default coordinate system to improve port transformations.
* Updates shapes and polygons to only include single polygons. Multiple polygons are now moved to the ``PolygonGroup`` class.
* Updated ports to extend from the vector class.
* Added a custom ``LayerList`` class that compares already added layers.
* Updated mixins to a single ``MixinBowl`` meta-configuration.
* Updated the datatype parameter of ports that represents primitive connects.
* Updated parameters to accept an extra restriction argument.
* Added ``NumberParameter`` which supports 'int' and 'float' parameters.
* Added ``ComplexParameter`` which supports 'int', 'float' and 'complex' parameters.
* Added automatic docstring generation.
* Fix type-checking implementation and updated parameter restrictions.

### Version 0.0.3 (March 12, 2019)
* Added Dummy ports for crossing nodes in netlist.
* Automatically generate terminal edges for metal polygons.
* Added shape for yTron.
* Added path routing between two terminals.
* Define a route using a list of terminals.
* Device cell detection (Junction, Via, etc).
* Basic LVS implementation.

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
