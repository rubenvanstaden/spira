Defining ports in a layout is done using the `create_ports` class method. 
Ports are objects that connect vertically, such as vias, and terminals 
are ports that connect horizontally. In this example a basic transmissionline 
is created with two ports connected to the endpoints.

**Demonstrates**

1. How ports are added to a cell.
2. How terminals are added to a cell.
3. Creating a box shape and converting it to a polygon elemental.
4. Extend a cell using inheritance.

Example `run_ports_1.py` shows how a cell can be extending using inheritance.
This is one of the functamental reasons for implementing the `create_` methods
in the SPiRA framework. It allows us to effectively segragate data members.


