# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 23:41:07 2022

@author: sbroggio
"""

import gdspy
import Utility

class Metamaterial:
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("metamaterial")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        
    def drawMetamaterial_fromgds(self):
        self.cell = Utility.importgds()
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)