#########
Framework
#########



******************
Process Design Kit
******************

The process design kit (PDK) is a set of technology files needed to implement
the physical aspects of a layout design. Application-specific rules specified
in the PDK controls how physical design applications work.

A new PDK scheme is introduced. The Python programming language is used to
bind PDK data to a set of classes, called data trees, that uniquely categorises
PDK data. This new PDK scheme is called the Rule Deck Database (RDD), also
refered to as the Rule Design Database. By having a native PDK in Python it
becomes possible to use methods from the SPiRA framework to create a
more descriptive PDK database. A design process typically contains the
following aspects:

* *GDSII Data*: Contains general settings required by the GDSII library, such as grid size.
* *Process Data*: Contains the process layers, layer purposes, layer parameters, and layer mappings.
* *Virtual Modelling*: Define derived layers that describes layer boolean operations.


Initialization
==============

All caps are used to represent the *RDD* syntax. The reason being to make the
script structure clearly distinguishable from the rest of the framework source
code. First, the RDD object is initialized, followed by the process name and
description. Second, the GDSII related variables are defined.

.. code-block:: python

    RDD.GDSII = ParameterDatabase()
    RDD.GDSII.UNIT = 1e-6
    RDD.GDSII.GRID = 1e-12
    RDD.GDSII.PRECISION = 1e-9


Process Data
============

.. ---------- Define Processes ----------

Define Processes
----------------

The first step in creating a layer is to define the process step that
it represents in mask fabrication. The layer process defines a specific
fabrciation function, for examples **metalization**. There can be multiple
different drawing layers for a single process. A *Process* database object
is created that contains all the different process steps in a specific
fabrication process:

.. code-block:: python

    RDD.PROCESS = ProcessLayerDatabase()

    RDD.PROCESS.GND = ProcessLayer(name='Ground Plane', symbol='GND')
    RDD.PROCESS.SKY = ProcessLayer(name='Sky Plane', symbol='SKY')
    RDD.PROCESS.R5 = ProcessLayer(name='Resistor 1', symbol='R5')
    RDD.PROCESS.M1 = ProcessLayer(name='Metal 1', symbol='M1')

Each process has a name that describes the process function, and
a *symbol* that is used to identify the process.

.. ---------- Define Purposes ----------

The purpose indicates the use of the layer. Multiple layers with
the same process but different purposes can be created. Purposes are defined
using a *Purpose* database object:

.. code-block:: python

    RDD.PURPOSE = PurposeLayerDatabase()

    RDD.PURPOSE.GROUND = PurposeLayer(name='Ground plane polygons', symbol='GND')
    RDD.PURPOSE.METAL = PurposeLayer(name='Polygon metals', symbol='METAL')
    RDD.PURPOSE.ROUTE = PurposeLayer(name='Metal routes', symbol='ROUTE')
    RDD.PURPOSE.RESISTOR = PurposeLayer(name='Polygon resistor', symbol='RES')

Similar to a **process** value each purpose contains a name and a unique symbol.

.. ---------- Process Parameters ----------

Parameters are added to a process by creating a *parameter* database object
that has a key value equal to the symbol of a pre-defined process:

.. code-block:: python

    RDD.M5 = ParameterDatabase()
    RDD.M5.MIN_SIZE = 0.7
    RDD.M5.MAX_WIDTH = 20.0
    RDD.M5.J5_MIN_SURROUND = 0.5
    RDD.M5.MIN_SURROUND_OF_I5 = 0.5

Any number of variables can be added to the tree using the dot operator.
The code above defines a set of design parameters for the *M5* process.

.. ---------- Physical Layers ----------

*Physical Layers* are unique to SPiRA and is defined as a layer that has a
defined process and purpose. A physical layer (PLayer) defines the different
purposes that a single process can be used for in a layout design.

.. code-block:: python

    RDD.PLAYER.M6 = PhysicalLayerDatabase()

    RDD.PLAYER.I5.VIA = PhysicalLayer(process=RDD.PROCESS.I5, purpose=RDD.PURPOSE.VIA)

    RDD.PLAYER.M6.METAL = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.METAL)
    RDD.PLAYER.M6.HOLE = PhysicalLayer(process=RDD.PROCESS.M6, purpose=RDD.PURPOSE.HOLE)

The code above illustrated the different purposes that process layer
**M6** can have in a layout design.

Virtual Modelling
~~~~~~~~~~~~~~~~~

*Derived Layers* are used to define different PLayer boolean operations.
They are typically used for virtual modelling and polygon operations,
such as merged polygons or polygon holes.

.. code-block:: python

    RDD.PLAYER.M5.EDGE_CONNECTED = RDD.PLAYER.M5.METAL & RDD.PLAYER.M5.OUTSIDE_EDGE_DISABLED
    RDD.PLAYER.M6.EDGE_CONNECTED = RDD.PLAYER.M6.METAL & RDD.PLAYER.M6.OUTSIDE_EDGE_DISABLED

The code above defines a derived layer that is generated when a layer with
process **M5** and purpose metal overlaps the outside edges of a all
process **M5** layers.


.. ---------------------------------------------------------------


Parameters
----------

When we’re designing PCells we need to model its parameters. An important characteristic
of a parameter is that it often only accepts a select range of values. When the parameter
corresponds to something physical the value often makes no sense when it’s zero or negative.
To avoid that users create designs which have no meaning, we want to inhibit that the user
assigns an invalid value to the parameter. This is exactly what we use properties for:
restricting the range and type of values you can assign to a parameter

In addition IPKISS’ properties help you as well with the following tasks:

* providing defaults for your parameters
* adding documentation for your parameters
* implement caching to ensure that calculations don’t need to be run twice ( when not required )

Define Parameters
~~~~~~~~~~~~~~~~~

Parameters are derived from the ``Parameter`` class. The
``ParameterInitializer`` is responsible for storing the parameters of an
instance. To define parameters the class has to inherit from the ``ParameterInitializer``
class. The following code creates a layer object with a number as a parameter.

.. code-block:: python

    import spira.all as spira
    class Layer(spira.ParameterInitializer):
        number = spira.Parameter()

    >>> layer = Layer(number=9)
    >>> layer.number
    9

At first glance this may not seem to add any value that default Python already adds.
The same example can be generated using native Python:

.. code-block:: python

    class Layer(object):
        def __init__(self, number=0):
            self.number = number

The true value of the parameterized framework comes into play when adding
parameter attributes, such as the **default** value, **restrictions**,
**preprocess** and **doc**. With these attributes parameters can be
type-checked and documented using customized values.

.. code-block:: python

    import spira.all as spira
    class Layer(spira.ParameterInitializer):
        number = spira.Parameter(default=0,
                                 restrictions=spira.INTEGER,
                                 preprocess=spira.ProcessorInt(),
                                 doc='Advanced parameter.')

The newly defined parameter has more advanced features that makes for
a more powerful design framework:

.. code-block:: python

    >>> layer = Layer()
    >>> layer.number
    0
    >>> layer.number = 9
    >>> layer.number
    9
    >>> layer.number = '8'
    >>> layer.number
    8
    >>> layer.number = 'Hi'
    ValueError:


Default
~~~~~~~

When defining a parameter the default value can be explicitly set using
the ``default`` attribute. This is a simple method of declaring your parameter.
For more complex functionality the default function attribute, ``fdef_name``,
can be used. This attribute defines the name of a class method that is used To
derive the default value of the parameter. Advantages of this technique is:

* **Logic operations:** The default value can be derived from other defined parameters.
* **Inheritance:** The default value can be overwritten using class inheritance.


.. code-block:: python

    import spira.all as spira
    class Layer(spira.ParameterInitializer):
        number = spira.Parameter(default=0)
        datatype = spira.Parameter(fdef_name='create_datatype')

        def create_datatype(self):
            return 1

    >>> layer = Layer()
    >>> (layer.number, layer.datatype)
    (0, 1)


Restrictions
~~~~~~~~~~~~

**Restrictions** are Python objects that validates the received value of a parameter.
In certain cases we want to restrict a parameter value to a certain type or range
of values, for example:

* Validate that the value is of specific object.
* Validate that the value falls between then minimum and maximum.

.. code-block:: python

    import spira.all as spira
    class Layer(spira.ParameterInitializer):
        number = spira.Parameter(default=0,
                                 restrictions=spira.RestrictRange(2,5))

The example above restricts the number parameter of the layer to be between 2 and 5:

.. code-block:: python

    >>> layer = Layer()
    >>> layer.number = 3
    3
    >>> layer.number = 1
    ValueError:

Preprocessors
~~~~~~~~~~~~~

**Preprocessors** converts a received value before assigning it to the parameter.
Preprocessors are typically used to convert a value of invalid type to one of
a valid type, such as converting a float to an integer.

Cache
~~~~~

SPiRA automatically caches parameters once they have been initialized.
When using class methods to define default parameters using the ``fdef_name``
attribute, the value is stored when called for the first time. Calling this
value for the second time will not lead to a re-calculation, but rather the
value will be retrieved from the cached dictionary.

The cache is automatically cleared when **any** parameter in the class is
updated, since other parameters might be dependent on the changed parameters.

.. ---------------------------------------------------------------

Parameterized Cells
-------------------

The SPiRA definition of a Parameterized Cell (PCell) in general terms:

    A PCell is a cell that defines how layout elementals must be generated.
    When instantiated it constructs itself according to the defined parameters.

GDSII layouts encapsulate elemental design in the visual domain. Parameterized cells encapsulates elementals in the programming domain, and utilizes this domain to map external data to elementals.
This external data can be data from the PDK or values extracted from an already designed layout using simulation software, such as InductEx.
The SPiRA framework uses a scripting framework approach to connect the visual domain with a programming domain.
The implemented architecture of SPiRA mimics the physical layout patterns implicit in hand-designed layouts.
This framework architecture evolved by developing code heuristics that emerged from the process of creating a PCell.

Creating a PCell is done by defining the elements and parameters required to create the desired layout.
The relationship between the elements and parameters are described in a template format.
Template design is an innate feature of parameterizing cell layouts.
This heuristic concludes to develop a framework to effectively describe the different constituents of a PCell, rather than developing an API.
The SPiRA framework was built from the following concepts:

1. **Defining Element Shapes** This step defines the geometrical shapes from which an element polygon is generated.
The supported shapes are rectangles, triangles, circles, as well as regular and irregular polygons.
Each of these shapes has a set of parameters that control the pattern dimensions, e.g. the parameterized rectangle has two parameters, width and length , that defines its length and width, respectively.

2. **Element Shape Transformations** This step describes the relation between the elements through a set of operations, that includes transformations of a shape in the x-y plane.
Transforming an element involves: movement with a specific offset relative to its original location, rotation of a shape around its center with a specific angle,
reflection of a shape around a idefined line, and aligning a shape to another shape with a specific offset and angle.

3. **PDK Binding** The final step is binding data from the PDK to each created pattern. In SPiRA data from the PDK is parsed into the RDD.
From this database the required process data can be linked to any specific pattern, such as the layer type of the defined rectangle, by defining
parameters and placing design restrictions on them.

Shapes
~~~~~~


.. code-block:: python

    class ShapeExample(spira.Cell):

        def create_elementals(self, elems):
            pts = [[0, 0], [2, 2], [2, 6], [-6, 6], [-6, -6], [-4, -4], [-4, 4], [0, 4]]
            shape = spira.Shape(points=pts)
            elems += spira.Polygon(shape=shape, layer=spira.Layer(1))
            return elems


Elements
~~~~~~~~

In the aboth example the ``spira.Polygon`` class was used to connect the shape with GDSII-related data, such as a layer number.
This is the purpose of elementals; to wrap geometry data with GDSII layout data.
In SPiRA the following elementals are defined:

* **Polygon**: Connects a shape object with layout data (layer number, datatype).
* **Label**: Generates text data in a GDSII layout.
* **SRef**: A structure references, or sometimes called a cell reference, refers to another cell object, but with difference transformations.

There are other special shapes that can be used in the pattern creation.
These shapes are mainly a combination polygons and relations between polygons.
These special shapes are referenced as if they represent a single shape and its outline is determined by its bounding box dimensions.
The following elemental groups are defined in the SPiRA framework:

* **Cells**: Is the most generic group that binds different parameterized elementals or clusters, while conserving the geometrical relations between these polygons or clusters.
* **Group**: A set of elementals can be grouped in a logical container, called ``Group``.
* **Ports**: A port is simply a polygon with a label on a dedicated process layer. Typically, port elementals are placed on conducting metal layers.
* **Routes**: A route is defined as a cell that consists of a polygon elemental and a set of edge ports, that resembles a path-like structure.

Group
~~~~~

Groups are used to apply an operation on a set of polygons, such a retrieving their combined bounding box.
The following example illistrated the use of ``Group`` to generate a metal bounding box around a set of polygons:

.. code-block:: python

    class GroupExample(spira.Cell):

        def create_elementals(self, elems):

            group = spira.Group()
            group += spira.Rectangle(p1=(0,0), p2=(10,10), layer=spira.Layer(1))
            group += spira.Rectangle(p1=(0,15), p2=(10,30), layer=spira.Layer(1))

            group.transform(spira.Rotation(45))

            elems += group

            bbox_shape = group.bbox_info.bounding_box(margin=1)
            elems += spira.Polygon(shape=bbox_shape, layer=spira.Layer(2))

            return elems

Ports
~~~~~

Port objects are unique to the SPiRA framework and are mainly used for connection purposes.

.. code-block:: python

    class PortExample(spira.Cell):

        def create_elementals(self, elems):
            elems += spira.Rectangle(p1=(0,0), p2=(20,5), layer=spira.Layer(1))
            return elems

        def create_ports(self, ports):
            ports += spira.Port(name='P1', midpoint=(0,2.5), orientation=180)
            ports += spira.Port(name='P2', midpoint=(20,2.5), orientation=0)
            return ports

Routes
~~~~~~



PCell creation is broken down into the following basic steps:

.. code-block:: python

    class PCell(spira.Cell):
        """ My first parameterized cell. """

        # Define parameters here.
        number = spira.IntegerParameter(default=0, doc=’Parameter example number.’)

        def create_elementals(self, elems):
            # Define elementals here.
            return elems

        def create_ports(self, ports):
            # Define ports here.
            return ports

.. code-block:: python

    >>> pcell = PCell()
    [SPiRA: Cell] (name ’PCell’, elementals 0, ports 0)
    >>> pcell.number
    0
    >>> pcell.__doc__
    My first parameterized cell.
    >>> pcell.number.__doc__
    Parameter example number.

The most basic SPiRA template to generate a PCell is shown above, and consists of three parts:

1. Create a new cell by inheriting from ``spira.Cell``. This connects the class to the SPiRA framework when constructed.

2. Define the PCell parameters as class attributes.

3. Elementals and ports are defined in the ``create_elementals`` and ``create_ports`` class methods, which is automatically added to the cell instance.
   The create methods are special SPiRA class methods that specify how the parameters are used to create the cell.


.. code-block:: python

    class Box(spira.Cell):

        width = param. NumberField(default=1)
        height = param. NumberField(default=1)
        gds_layer = param. LayerField(number=0, datatype=0)

        def create_elementals(self, elems):
            shape = shapes.BoxShape(width=self.width, height=self.height)
            elems += spira.Polygon(shape=shape, gds_layer=self.gds_layer)
            return elems

        def create_ports(self, ports):
            ports += spira.Port(name='Input', midpoint=(-0.5,0), orientation=90)
            ports += spira.Port(name='Output', midpoint=(0.5,0), orientation=270)
            return ports

.. code-block:: python

    >>> box = Box()
    [SPiRA: Cell] (name ’Box ’, width 1, height 1, number 0, datatype 0)
    >>> box.width
    1
    >>> box. height
    1
    >>> box. gds_layer
    [SPiRA Layer] (name ’’, number 0, datatype 0)


The above example illustrates constructing a parameterized box using the proposed framework:
First, defining the parameters that the user would want to change when creating a box instance.
Here, three parameter are given namely, the width, the height and the layer properties for GDSII construction.
Second, a shape is generated from the defined parameters using the shape module.
Third, this box shape is added as a polygon elemental to the cell instance.
This polygon takes the shape and connects it to a set of methods responsible for converting it to a GDSII elemental.
Fourth, two terminal ports are added to the left and right edges of the box, with their directions pointing away from the polygon interior.


Validate-by-Design
------------------



