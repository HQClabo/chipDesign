# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 17:36:40 2022

@author: sbroggio
"""


import gdspy
import Utility


class FeedLine:
    def __init__(self, coord_x, coord_y, rotation):
        
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("feedLine")
        celltemp = lib.new_cell("tempcell")
                
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        self.celltemp = celltemp
        
    def setParameters(self, init_cord,cord1,cord2,last_cord,Wm,Radius,offset):
        self.init_cord = init_cord
        self.cord1 = cord1
        self.cord2 = cord2
        self.last_cord = last_cord
        self.Wm = Wm
        self.Radius = Radius
        self.offset = offset

    def drawFeedLine(self):
    
    
        Coordinates1 = []
        Coordinates1.append(self.init_cord)
        Coordinates1.append(self.cord1)
        Coordinates1.append(self.cord2)
        Coordinates1.append(self.last_cord)
    
    
            
        feedLine = gdspy.FlexPath(Coordinates1,[self.offset,self.offset], self.Wm + self.offset, corners="circular bend", bend_radius=self.Radius, gdsii_path=True)
        self.cell.add(feedLine)
    
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)