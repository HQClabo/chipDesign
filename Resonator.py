# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 11:58:02 2022

@author: sbroggio
"""

import gdspy
import numpy as np
import Utility
#chipDesign.Utility as 

class Resonator:
    
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("Resonator")
        celltemp = lib.new_cell("tempcell")
        
    
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        self.celltemp = celltemp
      
        
    def getParameters(self):
        print(self.__dict__)
        
    def setParameters(self, length, initLength, terminationLength, radius, spacing, width, spacingDown, spacingUp, maxHeight):
        self.length = length
        self.initLength = initLength
        self.terminationLength = terminationLength
        self.radius = radius
        self.spacing = spacing
        self.width = width
        self.spacingDown = spacingDown
        self.spacingUp = spacingUp
        self.maxHeight = maxHeight
        
    def drawResonator(self):
        Heff = self.maxHeight - self.spacingDown - self.spacingUp
        Hefft = 2*self.radius + self.width + 2*self.spacing
        cnt = 0
        while Hefft < Heff :
            Hefft += 2*self.radius
            cnt += 1
        Htemp = Hefft - 4*self.radius
        Hend = Heff - Htemp
        Ltail = Hend - self.radius
        Lw = (self.length - self.initLength - np.pi*self.radius - (cnt-2)*np.pi*self.radius - self.terminationLength - np.pi*self.radius/2 - Ltail - self.width/2)/(cnt-2)

        cnteff = cnt - 2
        path1 = gdspy.Path(self.width, (0, self.spacingDown + self.width/2 + self.spacing ), number_of_paths=1)

        path1.segment(self.initLength, "+x")
        p0 = path1.length
        path1.turn(self.radius, "ll")

        if ( cnteff % 2 == 0):
            for turn in range (1,int( cnteff /2)+1):

                path1.segment(Lw, "-x")
                path1.turn(self.radius, "rr")
                path1.segment(Lw, "+x")
                path1.turn(self.radius, "ll")

            path1.segment(self.terminationLength)
            path1.turn(self.radius, "r")
            path1.segment(Ltail + self.width/2, "+y")
        else:
            for turn in range (1,int( cnteff/2)+1):

                path1.segment(Lw, "-x")
                path1.turn(self.radius, "rr")      
                path1.segment(Lw, "+x")
                path1.turn(self.radius, "ll")
                
            path1.segment(Lw, "-x")
            path1.turn(self.radius, "rr")
            path1.segment(self.terminationLength)
            path1.turn(self.radius, "l")
            path1.segment(Ltail + self.width/2, "+y")

        v = path1.length
        print(v)
        self.celltemp.add(gdspy.boolean(path1,None,"or",max_points=0))
        pathtemp = gdspy.CellReference(self.celltemp)

        off = gdspy.offset(pathtemp, self.spacing)
        self.cell.add(gdspy.boolean(off,pathtemp, "not"))
        
        

        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)

        
        
        
        
        
        
        