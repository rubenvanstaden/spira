gdspy
=======

The `gdspy <https://github.com/rubenvanstaden/gdspy>`_ package is a 
new package introduced for solving LVS problems for memory cell technology. 
It is a fork from the open source GDSPY library with multiple bug-fixes 
and some added extensions. A list of changes made to in this fork is given below:

1. When the top-level cell is flattened all labels are recursively added in position to the flattened structure. 
2. The labels positions added to the layout must be updated when the CellReference is reflected and/or translated. 
3. Support for calculating the bounding box of a polygon is added. 
4. Rotation algorithms are updated to support any angle and increments of 90 degrees.
