Getting Started
===============

GDSII files contain a hierarchical representation of any polygonal geometry.
They are mainly used in the microelectronics industry for the design of mask layouts, but are also employed in other areas.

Because it is a hierarchical format, repeated structures, such as identical transistors, can be defined once and referenced multiple times in the layout, reducing the file size.

There is one important limitation in the GDSII format: it only supports `weakly simple polygons <https://en.wikipedia.org/wiki/Simple_polygon>`_, that is, polygons whose segments are allowed to intersect, but not cross.

In particular, curves and shapes with holes are *not* directly supported.
Holes can be defined, nonetheless, by connecting their boundary to the boundary of the enclosing shape.
In the case of curves, they must be approximated by a polygon.
The number of points in the polygonal approximation can be increased to better approximate the original curve up to some acceptable error.

The original GDSII format limits the number of vertices in a polygon to 199.
Most modern software disregards this limit and allows an arbitrary number of points per polygon.
Gdspy follows the modern version of GDSII, but this is an important issue to keep in mind if the generated file is to be used in older systems.

The units used to represent shapes in the GDSII format are defined by the user.
The default unit in gdspy is 1 µm (10⁻⁶ m), but that can be easily changed by the user.


First GDSII
-----------

Let's create our first GDSII file:

.. code-block:: python

   import gdspy

   # Create the geometry: a single rectangle.
   rect = gdspy.Rectangle((0, 0), (2, 1))
   cell = gdspy.Cell('FIRST')
   cell.add(rect)

   # Save all created cells in file 'first.gds'.
   gdspy.write_gds('first.gds')

   # Optionally, display all cells using the internal viewer.
   gdspy.LayoutViewer()




