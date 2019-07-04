#########
Tutorials
#########


******************
Parameterized Cell
******************

Demonstrates
============

* How to create a parameterized cell by inheriting form ``spira.PCell``.
* How to add parameters to the cell.
* How to validate received parameters.

The first step in any SPiRA design environment is to import the framework:

.. code-block:: python

    import spira.all as spira

The ``spira`` namespace contains all the important functions and classes provided by the framework.
In order to create a layout cell all classes has to inherit from ``spira.PCell``:

.. code-block:: python

    class Resistor(spira.PCell):
        """ My first parameterized resistor cell. """

The ``spira.PCell`` class connects the design to the **SPiRA core**. In the exampe above we created
a parameterized cell of type ``Resistor`` and a basic description given in qoutation marks.
Now that a layout class has been constructed we need to define a set of *parameters* that will
describe how relations between layout elements in this class.

.. code-block:: python

    class Resistor(spira.PCell):
        """ My first parameterized resistor cell. """

        width = spira.FloatParameter(default=0.3, doc='Width of the shunt resistance.')
        length = spira.FloatParameter(default=1.0, doc='Length of the shunt resistance.')

We defined two parameters the ``width`` and the ``length`` of the resistor, along with a default
value equal to 0.3 and 1.0, respectively. Each parameter is also documented using the ``doc`` attribute.
As illistrated in this example the parameters are restricted to the ``float`` type. To check the validity
of the parameters is relation to eachother, we can use the ``validate_parameters`` method:

.. code-block:: python

    class Resistor(spira.PCell):
        """ My first parameterized resistor cell. """

        width = spira.FloatParameter(default=0.3, doc='Width of the shunt resistance.')
        length = spira.FloatParameter(default=1.0, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

The ``validate_parameters`` consists of a series of *if-statements* that check whether the defined
parameters are valid or not. Here, by definition we want to make sure the length of of the resistor
is larger than the width.

.. code-block:: python

    # 1. First create an instance of the resistor class.
    >>> D = Resistor()

    # 2. You van view the default values of the parameters.
    >>> (D.width, D.length)
    (0.3, 1.0)

    # 3. The parameter value is changed if it is valid.
    >>> D.width = 0.5
    >>> (D.width, D.length)
    (0.5, 1.0)

    # 4. Is an invalid value is received, an error is thrown.
    >>> D.width = 1.1
    ValueError: `Width` cannot be larger than `length`.


***********************
Connecting Process Data
***********************

Demonstrates
============

* How to connect fabrication process data to a design.
* How to change to a different fabrication process.

The ``RDD`` database is a SPiRA object that contains all the required data of a fabrication process.
SPiRA contains a default process that can be used directly from the ``spira`` namespace:

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

We updated the parameter default values to equal that of the minimum design restrictions defined
by the process for the resistor layer, ``R1``.

After having imported the ``spira`` namespace the default process database can be changed
by importing the desired ``RDD`` object.

.. code-block:: python

    import spira.all as spira
    from spira.technologies.mit.process.database import RDD

    >>> RDD
    <RDD MiTLL>


*****************
Creating Elements
*****************

Demonstrates
============

* How to add elements to a cell instance.
* How to create a shape geometry.
* How to create a GDSII polygon from a shape.

The ``create_elements`` class method is a unique SPiRA method that automatically connects
a list of elements to the class instance. Methods that starts with ``create_`` are special
methods in SPiRA and are called *create methods*.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_elements(self, elems):
            w, l = self.width, self.length
            shape = spira.Shape(points=[[0,0], [l,0], [l,w], [0,w]])
            elems += spira.Polygon(shape=shape, layer=spira.RDD.PLAYER.R1.METAL)
            return elems

The defined parameters are used to create a geometeric shape inside the ``create_elements`` method.
Once the shape is created it can be added to the layout as a polygon. The purpose of the ``Polygon``
class is to add GDSII-related data to an abstract geometry.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_elements(self, elems):
            elems += spira.Box(width=self.length, height=self.width, layer=spira.RDD.PLAYER.R1.METAL)
            return elems

Instead of manually creating shapes SPiRA offers a set of predefined polygons that can be used.
The code snippet above illustrates the use of the ``spira.Box()`` polygon instead of creating
a shape object and sending it the polygon container.


**************
Creating Ports
**************

Demonstrates
============

* How to connect ports to you layout.
* How to name and connect a process type to your port.
* How to unlock edge specific ports.

Similar to the ``create_elements`` method that connects element to your cell instance,
the ``create_ports`` method adds ports to your design. A port is defined as a vector object
that is used to connect different layout elements.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_elements(self, elems):
            elems += spira.Box(width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            w, l = self.width, self.length
            ports += spira.Port(name='P1_R1', midpoint=(-l/2,0), orientation=180, width=self.width)
            ports += spira.Port(name='P2', midpoint=(l/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)
            return ports

Port names has to be of the form *PortName_ProcessSymbol* is no process is added to the created object, as shown in
the example above with port ``P1_R1``. The process symbol set in the name are compared to the defined processes
in the RDD and automatically adds the process to the port object.

As shown with the ``P2`` the port name does not have to contain the process symbol is a process parameter
is added. The first letter of the port name defines its type. The 2 most important port types for PCell creation is:

* **P** (PinPort): The default port used as a terminal to horizontally connect different elements.
* **E** (EdgePort): Ports that are automatically generated from the edges of metal purpose layer polygons.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_elements(self, elems):
            elems += spira.Box(alias='ply1', width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            # Process symbol will automatically be added to the port name.
            ports += self.elements['ply1'].ports['E1_R1'].copy(name='P1')
            ports += self.elements['ply1'].ports['E3_R1'].copy(name='P2')
            return ports

Defining the exact midpoint of a port required knowledge of the boundary of the shape we want to connect to.
SPiRA automatically generates edge ports for metal polygons. The generated box element is given an alias
that is used to access that specific element. These edges can be activated as ports by simply changing
the port name. The example above illustrates changing edge port ``E1_R1`` to port ``P1``.


******
Routes
******

Demonstrates
============

* How to create a routes between two different ports.
* How to externally cache parameters.

Generally metal polygons are used to connect different circuit devices. In this example we first define
two ports and then generate a metal polygon between them using the ``spira.Route`` base class.
SPiRA offers a variaty of different routing algorithm depending on the relative position between
the ports. In this example we are generating a simple straight route, since the ports are already
horizontally aligned.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        p1 = spira.Parameter(fdef_name='create_p1')
        p2 = spira.Parameter(fdef_name='create_p2')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_p1(self):
            return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_p2(self):
            return spira.Port(name='P2', midpoint=(self.length/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_elements(self, elems):
            elems += spira.RouteStraight(p1=self.p1, p2=self.p2, layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            ports += [self.p1, self.p2]
            return ports

First, we define the ports as two separate parameters, ``p1`` and ``p2``. We use create methods to generate to ports
before adding them to the instance. Doing so allows us to access the port objects from both the ``create_elements``
method and the ``create_ports`` method.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        @spira.cache()
        def get_ports(self):
            p1 = spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)
            p2 = spira.Port(name='P2', midpoint=(self.length/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)
            return [p1, p2]

        def create_elements(self, elems):
            p1, p2 = self.get_ports()
            elems += spira.RouteStraight(p1=p1, p2=p2, layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            ports += self.get_ports()
            return ports

It is also possible to define all ports in a single method and externally cache the method using the ``spira.cache``
decorator as shown in the code snippet above.


**************
Cell Hierarchy
**************

Demonstrates
============

* How to create a manhattan route between two ports.
* How to use inheritance to mimic layout hierarchy.
* How to extend a layout without changing the parent class.
* How to pass cells as a parameter to another cell class.
* How to connect different structures using their ports.

.. code-block:: python

    class Resistor(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        p1 = spira.Parameter(fdef_name='create_p1')
        p2 = spira.Parameter(fdef_name='create_p2')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_p1(self):
            return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_p2(self):
            return spira.Port(name='P2', midpoint=(self.length/2,2), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_elements(self, elems):
            elems += spira.RouteManhattan(ports=[self.p1, self.p2], layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            ports += [self.p1, self.p2]
            return port

If two ports are not align on a single axis, the ``spira.RouteManhattan`` method can be used to
generate a manhattan polygon between them. One prerequisite is that the port orientations difference must
equal 180 degrees.

The created ``Resistor`` cell can be extende by creating a new cell that inherits from this class:

.. code-block:: python

    class ResistorExtended(Resistor):

        p3 = spira.Parameter(fdef_name='create_p3')

        def create_p3(self):
            return spira.Port(name='P3', midpoint=(self.length,0), orientation=90, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_elements(self, elems):
            elems = super().create_elements(elems)
            elems += spira.RouteManhattan(ports=[self.p2, self.p3], layer=spira.RDD.PLAYER.R1.METAL)
            return elems

To extend the elements we have to add the parent class elements to the current instance. This is done
using Python's ``super`` method: ``elems = super().create_elements(elems)``. A second route can then
be generated starting from ``p2`` and ending at ``p3``.

Another method to mimic cell hierarchy is to pass a cell to another cell as a parameter:


.. code-block:: python

    class ResistorManhattan(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        p1 = spira.Parameter(fdef_name='create_p1')
        p2 = spira.Parameter(fdef_name='create_p2')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_p1(self):
            return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_p2(self):
            return spira.Port(name='P2', midpoint=(self.length/2,2), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_elements(self, elems):
            elems += spira.RouteManhattan(ports=[self.p1, self.p2], layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            ports += [self.p1, self.p2]
            return ports


    class ResistorStraight(spira.PCell):

        width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
        length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

        p1 = spira.Parameter(fdef_name='create_p1')
        p2 = spira.Parameter(fdef_name='create_p2')

        def validate_parameters(self):
            if self.width > self.length:
                raise ValueError('`Width` cannot be larger than `length`.')
            return True

        def create_p1(self):
            return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_p2(self):
            return spira.Port(name='P2', midpoint=(self.length/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

        def create_elements(self, elems):
            elems += spira.RouteStraight(p1=self.p1, p2=self.p2, layer=spira.RDD.PLAYER.R1.METAL)
            return elems

        def create_ports(self, ports):
            ports += [self.p1, self.p2]
            return ports


    class ResistorConnect(spira.PCell):

        res0 = spira.CellParameter(default=ResistorManhattan)
        res1 = spira.CellParameter(default=ResistorStraight)

        def create_elements(self, elems):
            s1 = spira.SRef(reference=self.res0())
            s2 = spira.SRef(reference=self.res1())
            s2.connect(port=s2.ports['P1'], destination=s1.ports['P2'])
            elems += [s1, s2]
            return elem

We start by creating two resistor classes, ``ResistorManhattan`` and ``ResistorStraight``.
Then, we add them to a single cell instance were we can snap the two structures into place
by connecting their respective instance ports. A instance for each resistor cell is created
using ``spira.SRef`` and then ``P1`` of instance ``ResistorStraight`` is connect to ``P2``
of instance ``ResistorManhattan`` using the ``connect`` method.







