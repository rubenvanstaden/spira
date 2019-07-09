#################
Advanced Tutorial
#################

This set of tutorials focuses on explaining more advanced features that the SPiRA framework
has to over. We go into more details on how to create **device** and **circuit** PCells,
how to structure a design, and how to manipulate layout elements to create complex circuits.

*****
YTron
*****

In this example we will start from the beginning. First, we will create a *yTron* shape,
followed by using this shape to create a device that contains ports, and then using this
device to create a circuit that connect to input/output ports.

Demonstrates
============

* How to create your own shape class.
* How to create a device and a circuit PCell.
* How to restrict a design to only accept a specific shape or device.

We create our own yTron shape by inheriting from :py:class:`spira.Shape`, which allows us
to manipulate the shape once it has been instantiated.

.. code-block:: python

    class YtronShape(spira.Shape):
        """ Class for generating a yTron shape. """

        rho = NumberParameter(default=2, doc='Angle of concave bend between the arms.')
        arm_lengths = CoordParameter(default=(5,3), doc='Length or the left and right arms, respectively.')
        source_length = NumberParameter(default=5, doc='Length of the source arm.')
        arm_widths = CoordParameter(default=(2,2), doc='Width of the left and right arms, respectively.')
        theta = NumberParameter(default=10, doc='Angle of the left and right arms.')
        theta_resolution = NumberParameter(default=10, doc='Smoothness of the concave bend.')

        xc = Parameter(fdef_name='create_xc')
        yc = Parameter(fdef_name='create_yc')
        arm_x_left = Parameter(fdef_name='create_arm_x_left')
        arm_y_left = Parameter(fdef_name='create_arm_y_left')
        arm_x_right = Parameter(fdef_name='create_arm_x_right')
        arm_y_right = Parameter(fdef_name='create_arm_y_right')
        rad_theta = Parameter(fdef_name='create_rad_theta')
        ml = Parameter(fdef_name='create_midpoint_left')
        mr = Parameter(fdef_name='create_midpoint_right')
        ms = Parameter(fdef_name='create_midpoint_source')

        def create_rad_theta(self):
            return self.theta * np.pi/180

        def create_xc(self):
            return self.rho * np.cos(self.rad_theta)

        def create_yc(self):
            return self.rho * np.sin(self.rad_theta)

        def create_arm_x_left(self):
            return self.arm_lengths[0] * np.sin(self.rad_theta)

        def create_arm_y_left(self):
            return self.arm_lengths[0] * np.cos(self.rad_theta)

        def create_arm_x_right(self):
            return self.arm_lengths[1] * np.sin(self.rad_theta)

        def create_arm_y_right(self):
            return self.arm_lengths[1] * np.cos(self.rad_theta)

        def create_midpoint_left(self):
            xc = -(self.xc + self.arm_x_left + self.arm_widths[0]/2)
            yc = self.yc + self.arm_y_left
            return [xc, yc]

        def create_midpoint_right(self):
            xc = self.xc + self.arm_x_right + self.arm_widths[1]/2
            yc = self.yc + self.arm_y_right
            return [xc, yc]

        def create_midpoint_source(self):
            xc = (self.arm_widths[1] - self.arm_widths[0])/2
            yc = -self.source_length + self.yc
            return [xc, yc]

        def create_points(self, points):

            theta = self.theta * np.pi/180
            theta_resolution = self.theta_resolution * np.pi/180
            theta_norm = int((np.pi-2*theta)/theta_resolution) + 2
            thetalist = np.linspace(-(np.pi-theta), -theta, theta_norm)
            semicircle_x = self.rho * np.cos(thetalist)
            semicircle_y = self.rho * np.sin(thetalist)+self.rho

            xpts = semicircle_x.tolist() + [
                self.xc + self.arm_x_right,
                self.xc + self.arm_x_right + self.arm_widths[1],
                self.xc + self.arm_widths[1],
                self.xc + self.arm_widths[1],
                0, -(self.xc + self.arm_widths[0]),
                -(self.xc + self.arm_widths[0]),
                -(self.xc + self.arm_x_left + self.arm_widths[0]),
                -(self.xc + self.arm_x_left)
            ]

            ypts = semicircle_y.tolist() + [
                self.yc + self.arm_y_right,
                self.yc + self.arm_y_right,
                self.yc, self.yc - self.source_length,
                self.yc - self.source_length,
                self.yc - self.source_length,
                self.yc, self.yc + self.arm_y_left,
                self.yc + self.arm_y_left
            ]

            points = np.array(list(zip(xpts, ypts)))

            return points

There is a few important aspects to note in the :py:class:`YtronShape` class:

1. The :py:data:`create_points` create method is required by the :py:class:`spira.Shape` class and is similar
   to the :py:class:`create_elements` method for creating a cell.
2. In this example the importance of the :py:data:`doc` attribute when defining a parameter becomes apparent.
3. Using create methods to dynamically define the shape parameters makes the shape instance easier to use.

Once we have the desired shape we can use it to create a device cell, containing a GDSii layer and ports instances.

.. code-block:: python

    # ...

    class YtronDevice(spira.Device):

        shape = spira.ShapeParameter(restriction=spira.RestrictType([YtronShape]))

        def create_elements(self, elems):
            elems += spira.Polygon(shape=self.shape, layer=RDD.PLAYER.M1.METAL)
            return elems

        def create_ports(self, ports):

            left_arm_width = self.shape.arm_widths[0]
            rigth_arm_width = self.shape.arm_widths[1]
            src_arm_width = self.shape.arm_widths[0] + self.shape.arm_widths[1] + 2*self.shape.xc

            ports += spira.Port(name='Pl_M1', midpoint=self.shape.ml, width=left_arm_width, orientation=90)
            ports += spira.Port(name='Pr_M1', midpoint=self.shape.mr, width=rigth_arm_width, orientation=90)
            ports += spira.Port(name='Psrc_M1', midpoint=self.shape.ms, width=src_arm_width, orientation=270)

            return ports

    >>> shape = YtronShape(theta_resolution=100)
    >>> D = YtronDevice(shape=shape)
    >>> D.gdsii_output()

.. image:: _figures/_adv_0_ytron.png
    :align: center

The shape parameter defined in the :py:class:`YtronDevice` class restricts the PCell to only receive
a shape of type :py:class:`YtronShape`. Using the shape parameters the port instances for each arms
can be defined and added to the PCell instance.

The created yTron device can now be used in a circuit:

.. code-block:: python

    class YtronCircuit(spira.Circuit):

        ytron = spira.Parameter(fdef_name='create_ytron')

        @spira.cache()
        def get_io_ports(self):
            p1 = spira.Port(name='P1_M1', midpoint=(-10,10), orientation=0)
            p2 = spira.Port(name='P2_M1', midpoint=(5,10), width=0.5, orientation=270)
            p3 = spira.Port(name='P3_M1', midpoint=(0,-10), width=1, orientation=90)
            return [p1, p2, p3]

        def create_ytron(self):
            shape = YtronShape(rho=0.5, theta=5)
            D = YtronDevice(shape=shape)
            return spira.SRef(alias='ytron', reference=D)

        def create_elements(self, elems):
            p1, p2, p3 = self.get_io_ports()

            elems += self.ytron

            elems += spira.RouteManhattan(
                ports=[self.ytron.ports['Pl_M1'], p1],
                width=self.ytron.ref.shape.arm_widths[0],
                layer=RDD.PLAYER.M1.METAL,
                corners=self.corners)

            elems += spira.RouteStraight(p1=p2,
                p2=self.ytron.ports['Pr_M1'],
                layer=RDD.PLAYER.M1.METAL,
                path_type='sine', width_type='sine')

            elems += spira.RouteStraight(p1=p3,
                p2=self.ytron.ports['Psrc_M1'],
                layer=RDD.PLAYER.M1.METAL,
                path_type='sine', width_type='sine')

            return elems

        def create_ports(self, ports):
            ports += self.get_io_ports()
            return ports

The figure below shows the output of the yTron PCell is the class was constructed as a :py:class:`spira.PCell` layout.
The metal layers are separated and the connection ports are still visible.

.. image:: _figures/_adv_0_ytron_pcell.png
    :align: center

This figure is the final result when create a :py:class:`spira.Circuit` class rather than a PCell class.
The contacting metal layers are merged and the redundant ports are filtered.

.. image:: _figures/_adv_0_ytron_circuit.png
    :align: center

From the code above that generates this yTron circuit, we can see that three routes are defined.
The first, connects the left arm with the first port using a basic manhattan structure.
The second and third, connects the right arm to the second port and the source arm to the third port,
but uses a ``sine`` path type to generate the routing polygons.


**********
Via Device
**********

Demonstrates
============

* How to create a via device.
* How to add range restrictions to parameters.
* How to create a cell that validates design rules on instance creation.

Recall, that by definition a PCell script is responsible for describing the interrelations between
layout elements and defined parameters. These parameters can be design restrictions imposed by the
specific fabrication technology.

.. code-block:: python

    class ViaC5RA(spira.Device):
        """ Via component for the MiTLL process. """

        width = spira.NumberParameter(default=RDD.R5.MIN_SIZE, restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE))

        height = spira.Parameter(fdef_name='create_height')
        via_width = spira.Parameter(fdef_name='create_via_width')
        via_height = spira.Parameter(fdef_name='create_via_height')

        m6_width = spira.Parameter(fdef_name='create_m6_width', doc='Width of the via layer polygon.')
        m6_height = spira.Parameter(fdef_name='create_m6_height', doc='Width of the via layer polygon.')

        def create_m6_width(self):
            return (self.via_width + 2*RDD.C5R.M6_MIN_SURROUND)

        def create_via_width(self):
            return (self.width + 2*RDD.C5R.R5_MAX_SIDE_SURROUND)

        def create_via_height(self):
            return RDD.C5R.MIN_SIZE

        def create_height(self):
            return self.via_height + 2*RDD.R5.C5R_MIN_SURROUND

        def create_elements(self, elems):
            elems += spira.Box(layer=RDD.PLAYER.C5R.VIA, width=self.via_width, height=self.via_height, enable_edges=False)
            elems += spira.Box(alias='M6', layer=RDD.PLAYER.M6.METAL, width=self.m6_width, height=self.height, enable_edges=False)
            elems += spira.Box(alias='R5', layer=RDD.PLAYER.R5.METAL, width=self.width, height=self.height, enable_edges=False)
            return elems

        def create_ports(self, ports):
            p0 = self.elements['M6'].ports.unlock
            p1 = self.elements['R5'].ports.unlock
            return ports

Simply put, The code for the via PCell defined above is responsible for describing how the top and bottom metal layers
must be constructed in relation to the contact layer without violating any design rules. The PCell defines the specific
design rules applicable to the creation of this via device.


****************
Resistor Circuit
****************



Demonstrates
============

* How to design a circuit that can interchange different via devices.
* How to restrict the circuit to only accept vias of a certain type.
* How to activate specific port edges that can be used for external connetions.



.. code-block:: python

    class Resistor(spira.Circuit):
        """ Resistor PCell of type Circuit between two vias connecting to layer M6. """

        length = spira.NumberParameter(default=7)
        width = spira.NumberParameter(
            default=RDD.R5.MIN_SIZE,
            restriction=spira.RestrictRange(lower=RDD.R5.MIN_SIZE),
            doc='Width of the shunt resistance.')
        via = spira.CellParameter(
            default=dev.ViaC5RS,
            restriction=spira.RestrictType([dev.ViaC5RA, dev.ViaC5RS]),
            doc='Via component for connecting R5 to M6')
        text_type = spira.NumberParameter(default=92)

        via_left = spira.Parameter(fdef_name='create_via_left')
        via_right = spira.Parameter(fdef_name='create_via_right')

        def validate_parameters(self):
            if self.length < self.width:
                raise ValueError('Length cannot be less than width.')
            return True

        def create_via_left(self):
            via = self.via(width=0.3+self.width)
            T = spira.Rotation(rotation=-90)
            S = spira.SRef(via, transformation=T)
            return S

        def create_via_right(self):
            via = self.via(width=0.3+self.width)
            T = spira.Rotation(rotation=-90, rotation_center=(self.length, 0))
            S = spira.SRef(via, midpoint=(self.length, 0), transformation=T)
            return S

        def create_elements(self, elems):

            elems += [self.via_left, self.via_right]

            elems += RouteStraight(
                p1=self.via_left.ports['E0_R5'],
                p2=self.via_right.ports['E2_R5'],
                layer=RDD.PLAYER.R5.METAL)

            return elems

        def create_ports(self, ports):

            # FIXME: We do not want to connect to RES< but rather to M6.
            ports += self.via_left.ports['E1_M6'].copy(name='P1_M6')
            ports += self.via_left.ports['E2_M6'].copy(name='P2_M6')
            ports += self.via_left.ports['E3_M6'].copy(name='P3_M6')

            ports += self.via_right.ports['E0_M6'].copy(name='P4_M6')
            ports += self.via_right.ports['E1_M6'].copy(name='P5_M6')
            ports += self.via_right.ports['E3_M6'].copy(name='P6_M6')

            return ports

