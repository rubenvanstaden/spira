Tutorials
=========

The following tutorials will help you understand the basic methodology behind the 
SPiRA framework. This will show you how to use the framework to connect metadata 
to generated layout instances.

Parameterized Cells
-------------------

This examples defines the creation of a basic parameterized cell. By creating a new class that
inherits from the `spira.Cell` class. This connects the created class to the SPiRA gdsii
that binds parameters using a meta-configuration.

**Demonstrates**:

1. How to create a layout generator by inheriting from Cell.
2. How class attributes are defined as parameters.
3. The three different ways how a cell can be added to a library.

First we have to import the SPiRA framework and parameters namespace as follows:

.. code-block:: python
    :linenos:

    import spira
    from spira import param

Next, we can tell Python to create a PCell class by inheriting from `spira.Cell`. 
Parameters can be added to the PCell by defining class attributes using the `param` namespace.

.. code-block:: python
    :linenos:

    class PCell(spira.Cell):

        layer = param.LayerField(default=4)
        width = param.FloatField(default=1)

We can analyze the results as follow and connect the created cell to a library.
Using the `LOG` namespace allows to beatiful printing.

.. code-block:: python
    :linenos:

    from spira import LOG

    # Create a PCell instance.
    pcell = PCell()
    LOG.section('PCell instance')
    print(pcell)

    # When a cell is created it is automatically added
    # to SPiRA's default library class. The currently
    # set library can be retrieved and analyzed.
    from spira import settings
    lib_default = settings.get_library()
    LOG.section('Default library')
    print(lib_default)

    lib_new = spira.Library(name='New Lib')
    lib_new += pcell
    LOG.section('Create and add to new library')
    print(lib_new)


.. -----------------------------------------------------------------------------------


Database
--------

One the most powerful functionalities of SPiRA is effectively connect data to 
cell instances. This examples shows how data from the defined RDD can connected
to a PCell class using parameters. By connecting parameters to a class through a 
field allows the given data to be intersepted and manipulated before fully commiting
it to the class instance.

**Demonstrates**:

1. How to link process data from the RDD to default parameter values.
2. How to change parameters when creating an instance.
3. How to switch to a different RDD by simply importing a new database file.

The Rule Deck Database has to be imported before use. Importing a specific 
RDD script will initialize and create the data tree. The values can simply
be added using as normal parameters.

.. code-block:: python
    :linenos:

    from spira import RDD

    class PCell(spira.Cell):

        layer = param.LayerField(number=RDD.BAS.LAYER.number)
        width = param.FloatField(default=RDD.BAS.WIDTH)

Below is an example of changing the RDD to a different fabrication process.

.. code-block:: python
    :linenos:

    LOG.section('PCell paramters')
    pcell = PCell()
    print(pcell.layer)
    print('width: {}'.format(pcell.width))

    LOG.section('Update parameters')
    pcell = PCell(width=3.4)
    print('width: {}'.format(pcell.width))

    LOG.section('Switch to different RDD')
    print(RDD)
    from demo.pdks.process.aist_pdk import database
    print(RDD)


.. -----------------------------------------------------------------------------------


Elementals
----------

Now that we have a basic understanding of creating a cell and connecting data to an instance,
we have to add layout elementals to represent GDSII primitives. All elementals defined in the 
`create_elementals` method are automatically added to the instance.

**Demonstrates**:

1. How to add elementals to a cell using the `create_elementals` method.
2. Create a polygon using the framework and add it to the cell.
3. How to use the parameters when creating elementals.
4. How to write to a GDSII file.

.. code-block:: python
    :linenos:

    class PCell(spira.Cell):

        layer = param.LayerField(number=RDD.BAS.LAYER.number)
        width = param.FloatField(default=RDD.BAS.WIDTH)

        def create_elementals(self, elems):
            points = [[[0,0], [3,0], [3,1], [0,1]]]
            elems += spira.Polygons(polygons=points, gdslayer=self.layer)
            return elems

The result can be written to a GDSII file and viewed using the `gdspy` library.

.. code-block:: python
    :linenos:

    pcell = PCell()
    pcell.construct_gdspy_tree()


.. -----------------------------------------------------------------------------------


Subcells
--------

Cell references can be added to a cell using the `SRef` class. Created elementals can 
also be wrapped with another class and commited to a cell as a subcell.

**Demonstrates**:

1. How to create subcells in a pcell.
2. How to wrap elementals in a different cell what will 
   merge similar intersecting polygons.

The following example creates three polygons and then merges them using 
the functionality implicit in another defined class.

.. code-block:: python
    :linenos:

    from spira.lpe.structure import ComposeMLayers
    class PCell(spira.Cell):

        layer = param.LayerField(number=RDD.BAS.LAYER.number)
        width = param.FloatField(default=RDD.BAS.WIDTH)

        def create_elementals(self, elems):
            p0 = [[[0.3, 0.3], [3.6, 3]],
                [[1.45, 2.8], [2.45, 5]],
                [[1.25, 4.75], [2.65, 6]]]

            for points in p0:
                elems += spira.Rectangle(point1=points[0],
                                        point2=points[1],
                                        layer=self.layer)

            comp = ComposeMLayers(cell_elems=elems)
            elems += spira.SRef(comp)
            return elems


.. -----------------------------------------------------------------------------------


TemplateCells Basic
-------------------

This example demonstrates creating a via device.
Ports are automatically detected and added using
the StructureCell base class implicit in the framework.

**Demonstrates**:

1. Creating a via device.
2. A device is created using the Device class.

.. code-block:: python
    :linenos:

    class ViaPCell(spira.Cell):

        def create_elementals(self, elems):
            points = [[[0,0], [3,0], [3,1], [0,1]]]

            ply_elems = spira.ElementList()

            ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.BAS.LAYER)
            ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.COU.LAYER)
            ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.BC.LAYER)

            # Creates a device by sending the created 
            # elementals to the container cell.
            elems += spira.SRef(Device(cell_elems=ply_elems))
            return elems

    # ------------------------------ Scripts ------------------------------------

    via = ViaPCell()

    ViaTemplate().create_elementals(elems=via.elementals)

    via.construct_gdspy_tree()


.. -----------------------------------------------------------------------------------


TemplateCell Database
---------------------

This example shows the automatic creation of a via
device using the set variables from the RDD.

Demonstrates:
1. How to automate a PCell from the RDD.
2. DRC values can be set as parameters.


.. code-block:: python
    :linenos:

    class ViaPCell(spira.Cell):

        spacing = param.FloatField(default=RDD.BC.SPACING)

        def create_elementals(self, elems):
            
            ply_elems = spira.ElementList()

            ply_elems += spira.Box(center=(0,0), 
                                width=RDD.BAS.WIDTH,
                                height=RDD.BAS.WIDTH,
                                gdslayer=RDD.BAS.LAYER)
            ply_elems += spira.Box(center=(0,0), 
                                width=RDD.COU.WIDTH,
                                height=RDD.COU.WIDTH,
                                gdslayer=RDD.COU.LAYER)
            ply_elems += spira.Box(center=(0,0), 
                                width=RDD.BAS.WIDTH - self.spacing,
                                height=RDD.BAS.WIDTH - self.spacing,
                                gdslayer=RDD.BC.LAYER)
            elems += spira.SRef(Device(cell_elems=ply_elems))
            return elems

    # ------------------------------ Scripts ------------------------------------

    via = ViaPCell()

    ViaTemplate().create_elementals(elems=via.elementals)

    via.construct_gdspy_tree()




