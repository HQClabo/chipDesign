# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 10:31:59 2022

@author: jouanny
"""

import gdspy
import numpy as np
import Utility as uti

class squid_array:
    def __init__(self,n, coord_x, coord_y, rotation):
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        self.cell = lib.new_cell("SQUID")
        self.cell_array = lib.new_cell("SQUID_array")
        # self.cell_connectors = lib.new_cell("Connectors")
        self.n = n
        self.body_width = 4
        self.body_height = 5.2
        self.arms_width = 0.54
        self.arms_length = 1.35
        self.junction_height = 0.3
        self.junction_width = 0.64
        self.balcony_height = 0.5
        return print("SQUID array initialized")
    
    
    def set_parameters(self, body_width,body_height, arms_width, arms_length, junction_height, junction_width, balcony_height):
        self.body_width = body_width
        self.body_height = body_height
        self.arms_width = arms_width
        self.arms_length = arms_length
        self.junction_height = junction_height
        self.junction_width = junction_width
        self.balcony_height = balcony_height
        # return print("test")
    
    def __draw_body(self, layer = 2, datatype = 0):
        points = [[0,0],[0,self.body_height],[self.arms_width,self.body_height],[self.arms_width,self.body_height-self.arms_length],[self.body_width-self.arms_width,self.body_height-self.arms_length],[self.body_width-self.arms_width,self.body_height],
                  [self.body_width,self.body_height], [self.body_width,0], [self.body_width-self.arms_width,0], [self.body_width-self.arms_width,self.arms_length], [self.arms_width,self.arms_length], [self.arms_width,0], [0,0]]
        self.cell.add(gdspy.Polygon(points,layer = layer, datatype = datatype))
        
    def __draw_bridge(self, layer = 5, datatype = 0):
        junctionb1 = gdspy.Rectangle([self.arms_width/2-self.junction_width/2,-self.junction_height], [self.arms_width/2+self.junction_width/2,0],layer = layer, datatype = datatype)
        junctionb2 = gdspy.Rectangle([self.body_width - self.arms_width/2-self.junction_width/2,-self.junction_height], [self.body_width-self.arms_width/2+self.junction_width/2,0],layer = layer, datatype = datatype)
        junction1 = gdspy.Rectangle([self.arms_width/2-self.junction_width/2,self.body_height], [self.arms_width/2+self.junction_width/2,self.body_height+self.junction_height],layer = layer, datatype = datatype)
        junction2 = gdspy.Rectangle([self.body_width - self.arms_width/2-self.junction_width/2,self.body_height], [self.body_width-self.arms_width/2+self.junction_width/2,self.body_height+self.junction_height],layer = layer, datatype = datatype)
        self.cell_array.add(junctionb1)
        self.cell_array.add(junctionb2)
        self.cell.add(junction1)
        self.cell.add(junction2)
        
    def __draw_balcony(self, layer = 5, datatype = 0):
        balcony1 = gdspy.Rectangle([self.arms_width,self.arms_length-self.balcony_height],[self.body_width-self.arms_width,self.arms_length],layer = layer, datatype = datatype)
        balcony2 = gdspy.Rectangle([self.arms_width,self.body_height-self.arms_length],[self.body_width-self.arms_width,self.body_height-self.arms_length+self.balcony_height],layer = layer, datatype = datatype)
        self.cell.add(balcony1)
        self.cell.add(balcony2)
        
    def __draw_connectors(self,coord_x,coord_y, tail = 5, layer = 5, datatype = 0):
        points = np.array([[0,0], [self.body_width/2-self.arms_width,0], [self.body_width/2-self.arms_width,self.arms_length],
                           [self.body_width/2,self.arms_length],[self.body_width/2,-self.body_height/2+self.arms_length - tail],[-self.body_width/2,-self.body_height/2+self.arms_length- tail],
                           [-self.body_width/2,self.arms_length],[-self.body_width/2 + self.arms_width,self.arms_length],[-self.body_width/2 + self.arms_width,0],[0,0]])
        balcony = gdspy.Rectangle([-self.body_width/2+self.arms_width+coord_x,0+coord_y-self.arms_length],[self.body_width/2-self.arms_width+coord_x,self.balcony_height+coord_y-self.arms_length],layer = layer, datatype = datatype)
        connector = gdspy.Polygon(points+np.array([coord_x,coord_y])-np.array([0,self.arms_length]),layer = 2, datatype = 0)
        # self.cell_connectors.add(balcony)
        # self.cell_connectors.add(connector)
        
        # return gdspy.Polygon(points+np.array([coord_x,coord_y])-np.array([0,self.arms_length]))
        return balcony, connector
    
    
    def draw_squid_array(self):
        self.__draw_body()
        self.__draw_bridge()
        self.__draw_balcony()
        array = gdspy.CellArray(self.cell, 1, self.n, (0,self.body_height+self.junction_height))
        self.cell_array.add(array)
        array_points_init, array_points_final = self.cell_array.get_bounding_box()
        # connector1 = self.__draw_connectors(0,0)
        # connector1 = gdspy.CellReference(self.__draw_connectors(0,0),rotation = 0)
        # self.cell_array.add(connector1)
        # print(connector1)
        # connector1 = gdspy.CellReference(self.__draw_connectors((array_points_init[0]+array_points_final[0])/2,array_points_init[1]),rotation = 0)
        # self.cell_array.add(connector1)
        
        self.cell_array.add(self.__draw_connectors((array_points_init[0]+array_points_final[0])/2,array_points_init[1])[0])
        self.cell_array.add(self.__draw_connectors((array_points_init[0]+array_points_final[0])/2,array_points_init[1])[1])
        self.cell_array.add(self.__draw_connectors((array_points_init[0]+array_points_final[0])/2,array_points_final[1])[0].rotate(np.pi, center = ((array_points_init[0]+array_points_final[0])/2,array_points_final[1])))
        self.cell_array.add(self.__draw_connectors((array_points_init[0]+array_points_final[0])/2,array_points_final[1])[1].rotate(np.pi, center = ((array_points_init[0]+array_points_final[0])/2,array_points_final[1])))
        # return self.cell_array
        
        return uti.rotation(self.cell_array, self.coord_x, self.coord_y, self.rotation)
    # def extend_squid_array(self,height):
    #     box = self.cell_array.get_bounding_box()
    #     bottom_extension = gdspy.Rectangle([box[0][0],box[0][1]-height], [box[1][0],box[0][1]])
    #     self.cell_array.add(bottom_extension)
    
    
    # def output_design(self):
    #     self.draw_squid_array()
    #     return uti.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
        

# t = squid_array(32,0,0,0)
# # t.draw_body()
# # t.draw_bridge_balcony()
# # test = t.draw_squid_array()
# # test2 = uti.rotation(test, 0, 0, 90)

# body_width = 4
# body_height = 5.2
# arms_width = 0.54
# arms_length = 1.35
# junction_height = 0.3
# junction_width = 0.64
# balcony_height = 0.5
# t.set_parameters(body_width, body_height, arms_width, arms_length, junction_height, junction_width, balcony_height)
# t.draw_squid_array()
# # v = t.output_design(0,500)
# # t.extend_squid_array(8)
# gdspy.LayoutViewer()
