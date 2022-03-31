# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 15:49:37 2022

@author: sbroggio
"""

import gdspy
import Utility

class SquidJ:
    
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("squidJunction")
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib

        
    def setParametersSquid(self, squidLength, squidSpacing, lengthConnector , width, upspacing):
        self.squidLength = squidLength
        self.squidSpacing = squidSpacing
        self.lengthConnector = lengthConnector
        self.width = width
        self.upspacing = upspacing
        
    def setParametersPatch(self,topPatchCoord,topPatchCoord1, bottomPatchCoord, bottomPatchCoord1, rect, rect1):
        self.topPatchCoord = topPatchCoord
        self.bottomPatchCoord = bottomPatchCoord
        self.topPatchCoord1 = topPatchCoord1
        self.bottomPatchCoord1 = bottomPatchCoord1
        self.rect = rect
        self.rect1 = rect1
        
    
    """
    def drawSquidJline(self):
        path1 = gdspy.Path(self.width, (0,0), number_of_paths=2, distance = self.squidSpacing + self.width)
        path1.segment(self.squidLength,"+y")
        
        path2 = gdspy.Path(self.width, (-self.lengthConnector/2,self.squidLength/9), number_of_paths=1)
        path2.segment(self.lengthConnector)
        self.tempcell.add(path1)
        self.tempcell.add(path2)
        
        return Utility.rotation(self.tempcell, self.coord_x, self.coord_y, self.rotation)
    
    def drawTopPatch(self):
        gdspy.Rectangle([self.topPatchCoord[0],self.topPatchCoord[1]], [self.topPatchCoord1[0],self.topPatchCoord1[1]])
        return Utility.rotation(self.tempcell, self.coord_x, self.coord_y, self.rotation)

    def drawBottomPatch(self):
        gdspy.Rectangle([self.bottomPatchCoord[0],self.bottomPatchCoord[1]], [self.bottomPatchCoord1[0],self.bottomPatchCoord1[1]])
        return Utility.rotation(self.tempcell, self.coord_x, self.coord_y, self.rotation)"""   
    
    def drawSquidJ(self):
        path1 = gdspy.Path(self.width, (0,0), number_of_paths=2, distance = self.squidSpacing + self.width)
        path1.segment(self.squidLength,"+y")
        
        path2 = gdspy.Path(self.width, (-self.lengthConnector/2,self.squidLength-self.upspacing), number_of_paths=1)
        path2.segment(self.lengthConnector)
        self.cell.add(path1)
        self.cell.add(path2)
        
        self.cell.add(gdspy.Rectangle([self.topPatchCoord[0],self.topPatchCoord[1]], [self.topPatchCoord1[0],self.topPatchCoord1[1]]))
        self.cell.add(gdspy.Rectangle([self.bottomPatchCoord[0],self.bottomPatchCoord[1]], [self.bottomPatchCoord1[0],self.bottomPatchCoord1[1]]))
        self.cell.add(gdspy.Rectangle([self.rect[0],self.rect[1]],[self.rect1[0],self.rect1[1]]))  
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        
     