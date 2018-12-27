This examples defines the creation of a basic parameterized cell, by creating a new class that
inherits from the `spira.Cell` class. A meta-configuration is used to dynamically bind the 
class parameters to the cell instance. This examples defines the creation of a 
basic parameterized cell.

**Demonstrates**

1. How to create a layout generator by inheriting from Cell.
2. How class attributes are defined as parameters.
3. The three different ways a cell can be added to a library.

First we have to import the SPiRA framework and parameters namespace. 
Parameters can be added to the PCell by defining class attributes using the 
`param` namespace. Using the `LOG` namespace allows for beatiful printing.

