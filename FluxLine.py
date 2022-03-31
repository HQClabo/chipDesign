# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 11:32:18 2022

@author: sbroggio
"""
import numpy 
import gdspy
import Utility


class FluxLine:
    def __init__(self, coord_x, coord_y, rotation):
        
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("fluxLine")
        celltemp = lib.new_cell("tempcell")
        celltemp2 = lib.new_cell("tempcell2")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        self.celltemp = celltemp
        self.celltemp2 = celltemp2
        
    def setParameters(self, init_cord,cord1,cord2,last_cord,Wm,Radius,offset,Radius_term, coupling_len):
        self.init_cord = init_cord
        self.cord1 = cord1
        self.cord2 = cord2
        self.last_cord = last_cord
        self.Wm = Wm
        self.Radius = Radius
        self.offset = offset
        self.Radius_term = Radius_term
        self.coupling_len = coupling_len
        
    def drawTempFLuxline(self):
    
    
        Coordinates1 = []
        Coordinates1.append(self.init_cord)
        Coordinates1.append(self.cord1)
        Coordinates1.append(self.cord2)
        Coordinates1.append(self.last_cord)
    
    
            
        fluxLine = gdspy.FlexPath(Coordinates1,[self.offset,self.offset], self.Wm + self.offset, corners="circular bend", bend_radius=self.Radius, gdsii_path=True)
        self.celltemp.add(fluxLine)
        self.boundaries = self.celltemp.get_bounding_box()
        print(self.boundaries)
    
    
        return fluxLine
    
    
    def drawFluxLine(self):
        importedFluxline = FluxLine.drawTempFLuxline(self)
        #points = [(self.boundaries[0][0]-50,self.boundaries[0][1]-50), (self.boundaries[1][0] + 50 ,self.boundaries[0][1] - 50 ), (self.boundaries[1][0] + 50,self.boundaries[1][1]), (self.boundaries[0][0] - 50 , self.boundaries[1][1] )]
        points = [(self.boundaries[0][0],self.boundaries[0][1]), (self.boundaries[1][0] ,self.boundaries[0][1]), (self.boundaries[1][0],self.boundaries[1][1]), (self.boundaries[0][0], self.boundaries[1][1] )]
        ground = gdspy.Polygon(points)
        

        pos = gdspy.boolean(ground, importedFluxline, 'not')


        path1 = gdspy.Path(self.Wm , (self.last_cord), number_of_paths=2)

        path1.segment(0,'-x')
        path1.turn(self.Radius_term,"ll")

        #path1.segment(self.coupling_len,'+x')
        #path1.turn(self.Radius_term,"r")
        
        self.celltemp2.add(path1)
        
        bound2 = self.celltemp2.get_bounding_box()
        
        #pointsground2 = [(bound2[0][0] - 50 ,bound2[0][1]), (bound2[1][0] + 50 ,bound2[0][1]),(bound2[1][0] + 50 ,bound2[1][1] + 50), (bound2[0][0] - 50, bound2[1][1] + 50)]
        pointsground2 = [(bound2[0][0],bound2[0][1]), (bound2[1][0],bound2[0][1]),(bound2[1][0],bound2[1][1]), (bound2[0][0], bound2[1][1])]


        ground2 = gdspy.Polygon(pointsground2)
        #ground3 = gdspy.Polygon(pointsground3)


        s1 = gdspy.boolean(ground2,path1, 'not')
        s2 = gdspy.boolean(ground,pos, 'not')

        self.cell.add(s1)
        #self.cell.add(pos)
        self.cell.add(s2)
        #self.cell.add(ground)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)