<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/rubenvanstaden/spira">
    <img src="docs/_figures/spira_logo.png" alt="Logo" width="200" height="280">
  </a>

  <h3 align="center">Quantum Layout Design Environment</h3>

  <p align="center">
    The next-generation object-oriented script-based PCell design environment.
    <br />
    <a href="https://spira.readthedocs.io/en/latest/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/rubenvanstaden/spira/issues">Report Bug</a>
    ·
    <a href="https://github.com/rubenvanstaden/spira/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contribute](#contribute)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->
<!-- [![Product Name Screen Shot][product-screenshot]](docs/_figures/spira_logo.png) -->
![phidl example image](https://github.com/rubenvanstaden/spira/blob/master/docs/_figures/_adv_jtl_false.png)

**SPiRA** is the next-generation object-oriented script-based PCell design environment.
The framework leverages the Python programming language to effectively generate circuit layouts,
while simultaneously checking for design violations, through a novel methodology called *validate-by-design*. 
Creating PCells and extracting a model from a layout requires data from the fabrication process. 
A new PDK scheme is introduced, called the Rule Deck Database (RDD), that effectively connects
process data to the SPiRA framework. The design of the **RDD** revolves around the principle that
a PDK cannot be created, but rather that it evolves as our understanding of physical layout design evolves.

### Benefits of using SPiRA

* Create a PCell framework that is easy to use by designers with the focus falling on Superconducting and Quantum Integrated Circuits.
* Effectively connect process data to layout elements in a generic process-independent fashion.
* No specific programming knowledge is required.
* Easily share designs between colleagues.
* Created PCells can easily be included in a hand-designed layout.

### Features

* Define layout elements in a templated environment.
* Ability to leverage object-oriented inheritance to simply complex designs.
* Comprehensive set of commands for shape generation.
* Use port objects to connect different layout elements.
* Use routing algorithms to generate polygonal paths between devices.
* Meticulously define a technology process using Python.

A list of used resources that was helpful in the development of the SPiRA framework.

### Built With

Love



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them in Fedora:

```bash
sudo dnf install redhat-rpm-config
sudo dnf install gcc-c++
sudo dnf install python3-devel
sudo dnf install tkinter
sudo dnf install gmsh
```

### Installation

You can install SPiRA directly from the Python package manager *pip* using and remember to create a *virtual environment*:

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



<!-- USAGE EXAMPLES -->
## Usage

_For examples, please refer to the [Documentation](https://spira.readthedocs.io/en/latest/)_

All examples can be ran from the environment directory, which is the home directory of your ``spira`` folder.
For the basic tutorial samples:

```python
python tutorials/basic/_9_stretch_1.py
```

For the more advanced example with their own defined Rule Deck Database, as
explained [here](https://spira.readthedocs.io/en/latest/).

```python
python spira/technologies/default/circuits/ytron_circuit.py
```


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/rubenvanstaden/spira/issues) for a list of proposed features (and known issues).
As a short overview here is the project focus over the next 12 month:

* Complete netlist extraction and device detection from a native GDSII layout.
* Add graph isomorphic checks for differences between the extracted layout netlist and that of the designed SPICE netlist.
* Implement DRC algorithms and integration support with parameter extraction engines.


<!-- CONTRIBUTING -->
## Contribute

Contributions are what make the open source community such an amazing place to be learn, inspire, and create.
Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

* Ruben van Staden - rubenvanstaden@gmail.com
* Coenrad Fourie - coenradf@gmail.com  
* Kyle Jackman - kylejack1@gmail.com 
* Joey Delport - joeydelp@gmail.com 



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Gdspy](https://github.com/heitzmann/gdspy)
* [Phidl](https://github.com/amccaugh/phidl)
* [Clippers](http://www.angusj.com/delphi/clipper.php)



<!-- HISTORY OF CHANGES -->
## History of changes

### Version 0.2.0 (October 4, 2019)
* Added layout netlist extraction and viewing.
* Added electrical rule checking (ERC).
* Added **filters** for advanced layout manipulation.
* Updated ports for more information descriptions. Terminals can now be separated from port definitions.
* A new concept, called **virtual modeling** (VModel) is introduced. This allows you to create multiple, virtual versions of a single layout for either debugging or fabrication purposes.
* Routing algorithms have been updated to leverage speed improvements made in the Gdspy library.
* The GDSII parser has been updated for better code structure and faster read/write operations.

### Version 0.1.1 (July 16, 2019)
* Updated the advanced tutorial documentation.
* Added developers documentations.
* Updated the expand transform algorithms, which fixes a lot of known issues.
* Updated the GDSII input parser to use new transformation parameters.
* Changed the ``ref`` parameter to ``reference`` in ``SRef``.

### Version 0.1.0 (July 10, 2019)
* Added first version of documentation.
* Renamed ``Fields`` to ``Parameters`` to overcome confusion.
* Renamed ``elemental`` to ``elements``, since ``spira.Cell`` does not inherit from ``gdspy.Cell`` anymore.
* Added parameter restrictions and preprocessing capabilities.
* Updated parameters to accept an extra restriction argument.
* Introduces ``Vector``, ``Line``, and ``Coord`` classes.
* Depricated locked ports. Instead different port purposes can now be defined.
* Introduces *process* and *purpose* parameters to layer elements.
* Introduces *derived layers* to allow for layer boolean operations. This makes the RDD more flexible for future technology changes.
* Updated the edge generation algorithms to include both an outside and inside edge.
* Updated the routing algorithms to use new ``gdspy`` features.
* Added stretching operations.
* Extended the RDD to include *display resources*.
* Fix issues with writing to a GDSII file.
* Added snap to grid functionality.
* Implemented parameters caching.
* Added port alignment operations.
* Added `PortList` class for special port filtering functionality.
* Created layer mappers.
* Changed the default coordinate system to improve port transformations.
* Updates shapes and polygons to only include single polygons. Multiple polygons are now moved to the ``PolygonGroup`` class.
* Updated ports to extend from the ``Vector``.
* Added a custom ``LayerList`` class that compares already added layers.
* Updated mixins to a single ``MixinBowl`` meta-configuration.
* Updated the datatype parameter of ports that represents primitive connects.
* Added ``NumberParameter`` which supports 'int' and 'float' parameters.
* Added ``ComplexParameter`` which supports 'int', 'float' and 'complex' parameters.
* Added automatic docstring generation.

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



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=flat-square
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=flat-square
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=flat-square
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=flat-square
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png