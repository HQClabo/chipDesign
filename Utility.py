# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 16:05:36 2022

@author: sbroggio
"""
import gdspy


def rotation (celltoRotate,coord_x,coord_y,rotation):
    
    lib = gdspy.GdsLibrary()
    gdspy.current_library = lib
    
    outCell = lib.new_cell("rotatedCell")
    
    
    if rotation == 0:
        outCell.add(gdspy.CellReference(celltoRotate,(coord_x,coord_y), x_reflection = False, rotation = 0))
        outCell.flatten()
        return outCell
        
    elif rotation == 90:
        outCell.add(gdspy.CellReference(celltoRotate,(coord_x,coord_y), x_reflection = False, rotation = 90))
        outCell.flatten()
        return outCell
    elif rotation == -90: 
        outCell.add(gdspy.CellReference(celltoRotate,(coord_x,coord_y), x_reflection = False, rotation = -90))
        outCell.flatten()
        return outCell
    else: 
        outCell.add(gdspy.CellReference(celltoRotate,(coord_x,coord_y), x_reflection = False, rotation = 180))
        outCell.flatten()
    
        return outCell


def importgds():
    lib = gdspy.GdsLibrary()                                                                                     
    gdspy.current_library = lib
    
    importedlibmeta = lib.read_gds(r'\\files3\data\sbroggio\My Documents\Davide\Design\GDSPY\Metamaterial\Metamaterial.gds')
    cell = lib.new_cell("Chip")
    toplevelcell = importedlibmeta.top_level()
    cellmeta = importedlibmeta.extract(toplevelcell[0], overwrite_duplicate=True)
    cell.add(cellmeta)
    cell.flatten()
    
    return cell

def switchSign(celltoSwitch):
    lib = gdspy.GdsLibrary()
    gdspy.current_library = lib
    
    celltemp = lib.new_cell("celltemp")
    outCell = lib.new_cell("switchedCell")
    bound2 = celltoSwitch.get_bounding_box()
    pointsground2 = [(bound2[0][0],bound2[0][1]), (bound2[1][0],bound2[0][1]),(bound2[1][0],bound2[1][1]), (bound2[0][0], bound2[1][1])]
    ground2 = gdspy.Polygon(pointsground2)
    

    s1 = gdspy.boolean(ground2,celltoSwitch, 'not')
    outCell.add(s1)
    
    return outCell

def change_layer_of_entire_cell(cell, layer, datatype=None):
    """
    Changes layer and datatype of all polygonsets in a cell.

    Parameters
    ----------
    cell : gdspy.Cell
        Cell whose polygonsets are to be changed.
    layer : Integer
        Layer which will be assigned to polygonsets.
    datatype : Integer, optional
        Datatype which will be assigned to polygonsets. The default is None.

    Returns
    -------
    None.

    """
    # changes layer and datatype of all polygonsets of a cell

    # Get dependency cells recursively
    all_cells = cell.get_dependencies(True)
    # Include original cell in the set
    all_cells.add(cell)
    for c in all_cells:
        # Process all polygons
        for polygon in c.polygons:
            # Substitute layer list for a new one with the
            # the same length and the desired layer number
            polygon.layers = [layer] * len(polygon.layers)
            # Proecessing datatype
            if datatype != None:
                polygon.datatypes = [datatype] * len(polygon.layers)
        # Process all paths
        for path in c.paths:
            path.layers = [layer] * len(path.layers)
        # Process all labels
        for label in c.labels:
            label.layer = layer
 
def change_specific_layer(cell, layer_in, layer_out):
    """
    Changes polygonsets in a cell from layer_in to layer_out.

    Parameters
    ----------
    cell : gdspy.Cell
        Cell whose polygonsets are to be changed.
    layer_in : Integer
        Polygonsets in this layer will be assigned another.
    layer_out : Integer
        Layer which will be assigned the selected polygonsets.

    Returns
    -------
    None.

    """
    # changes layer and datatype of all polygonsets of a cell

    # Get dependency cells recursively
    all_cells = cell.get_dependencies(True)
    # Include original cell in the set
    all_cells.add(cell)
    for c in all_cells:
        # Process all polygons
        for polygon in c.polygons:
            if layer_in in polygon.layers:
                polygon.layers = [layer_out] * len(polygon.layers)        
        # Process all paths
        for path in c.paths:
            if layer_in in path.layers:
                path.layers = [layer_out] * len(path.layers)
        # Process all labels
        for label in c.labels:
            if layer_in in path.layers:
                label.layer = layer_out

def get_polygons_in_layer(cell_in, cell_out, layers):
    """
    Exctracts all polygonsets that are the specified layers from cell_in
    and copy them into cell_out.
    
    Parameters
    ----------
    cell_in : gdspy.Cell
        Cell from which you want to extract polygonsets.
    cell_out : gdspy.Cell
        Cell which will contain the extracted polygonsets.
    layers : List
        Cist of layers from which polygonsets are extracted.

    Returns
    -------
    cell_out : gdspy.Cell
        Cell which will contain the extracted polygonsets.

    """
    cell = cell_in.copy('temp_copy')

    cell.flatten()
    if type(layers)==int:
        layers = [layers]
    for layer in layers:
        # Process all polygons
        for polygon in cell.polygons:
            if layer in polygon.layers:
                cell_out.add(polygon)
            # Substitute layer list for a new one with the
            # the same length and the desired layer number
            # polygon.layers = [layer] * len(polygon.layers)
        # Process all paths
        for path in cell.paths:
            if layer in path.layers:
                cell_out.add(path)
        # Process all labels
        for label in cell.labels:
            if layer == label.layer:
                cell_out.add(label)
    gdspy.current_library.remove(cell)
    return cell_out
