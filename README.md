# SPiRA

**SPiRA** is the next-generation object-oriented script-based PCell design environment.
The framework leverages the Python programming language to effectively generate circuit layouts,
while simultaneously checking for design violations, through a novel methodology called *validate-by-design*. 
Creating PCells and extracting a model from a layout requires data from the fabrication process. 
A new PDK scheme is introduced, called the Rule Deck Database (RDD), that effectively connects
process data to the SPiRA framework. The design of the **RDD** revolves around the principle that
a PDK cannot be created, but rather that it evolves as our understanding of physical layout design evolves.

**Benefits of using SPiRA:**

* Create a PCell framework that is easy to use by designers with the focus falling on Superconducting and Quantum Integrated Circuits.
* Effectively connect process data to layout elements in a generic process-independent fashion.
* No specific programming knowledge is required.
* Easily share designs between different colleagues.
* Created PCells can easily be included in a hand-designed layout.

**Features:**

* Define layout elements in a templated environment.
* Ability to leverage object-oriented inheritance to simply complex designs.
* Comprehensive set of commands for shape generation.
* Use port objects to connect different layout elements.
* Use routing algorithms to connect polygon layer between devices.

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

The framework [documentation](https://spira.readthedocs.io/en/latest/) will get you started.
For more examples please contact Ruben van Staden <rubenvanstaden@gmail.com>.

## Known Issues
* There are some issues with reflection transformations.

## Future Changes
* Update polygon to include rounded corners.

## History of changes

### Version 0.1.0 (July 10, 2019)
* Added first version of documentation.
* Depricated locked ports with defining different port purposes.
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
