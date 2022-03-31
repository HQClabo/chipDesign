# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 16:21:52 2022

@author: sbroggio
"""

import gdspy
import Utility

class Capacitor_Coupling:
    
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("capacitor_Coupling")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        
    def setParameters(self, heigth, width, spacing):
        self.heigth = heigth
        self.width = width
        self.spacing = spacing
        
    def drawCapacitorArray(self):
        
        singleCapacitor = gdspy.Rectangle((-self.width/2,-self.heigth/2), (self.width/2, self.heigth/2))
        
        self.cell.add(singleCapacitor)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)