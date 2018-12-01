Cell Labels
===========

Using the gdspy library all cells in the GDS layout are recursively looped and 
if-statements are used to with the cell-type, which is the string in the 
beginning of the name of the cell (‘via\_’, ‘jj\_’, ‘ntron\_’, etc). 
All via cells are first detected and processed before looking to device 
cells, such as ntrons. The reason is because device cells can hierarchically 
include more via cells inside. Once a cell has been detected we enter the 
cell object and apply the following changes. The datatype variable linked to 
all layers in the cell are updated to a unique value that represents a cell type:

:: 

    0 - Normal interconnected wire layers in the top-level cell.
    1 - Layers that are inside via cells. 
    2 - Layers inside jj cells.
    3 - Layers inside ntron cells.

Ntron Detection 
---------------

As previously explained the default method for detecting devices is done by 
labeling the center of the cell, but in some cases this method fails. 
In non-symmetric cells the center coordinate might not fall inside any of the 
wire polygons and will thus fail detecting the triangle in the mesh. 
To solve this we get the bounding box of the ntron cell and create a polygon 
with a unique key value to it. Once the mesh is generate using the Auron 
package, we can detect all the nodes inside this bounding box polygon and label then as ntron-nodes.
