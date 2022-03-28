# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 18:16:29 2022

@author: sbroggio
"""
import gdspy
import Utility

class Waveguide:
    
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("fluxLine")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        
    def setParameters(self, width, spacing, length, radius, initLength):
        self.length = length
        self.radius = radius
        self.initLength = initLength
        self.width = width
        self.spacing = spacing
        
    def drawWaveguide(self):
        waveguidePath = gdspy.Path(self.width, (0, 0), number_of_paths=2, distance = self.spacing + self.width)
        waveguidePath.segment(self.initLength, "+y")
        waveguidePath.turn(self.radius, "r")
        waveguidePath.segment(self.length, "+x")
        waveguidePath.turn(self.radius, "r")
        waveguidePath.segment(self.initLength, "-y")
        
        self.cell.add(waveguidePath)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    