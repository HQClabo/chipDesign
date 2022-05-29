# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:03:11 2022

@author: sbroggio
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 15:06:27 2022

@author: sbroggio
"""

import gdspy
import numpy as np
import chipDesign.Utility as Utility

#kjfdkfjlkdfjdkf
class Pad:
    
    def __init__(self, coord_x, coord_y, rotation):
        
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("Pad")
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.lib = lib
        self.cell = cell

    def setParameters(self, width_pad, length_pad, pad_tail, width_waveguide, gnd_offset_pad, gnd_offset_waveguide, pad1 ):
        self.width_pad = width_pad
        self.length_pad = length_pad
        self.pad_tail = pad_tail
        self.width_waveguide = width_waveguide
        self.gnd_offset_pad = gnd_offset_pad
        self.gnd_offset_waveguide = gnd_offset_waveguide
        self.pad1 = pad1
        
    
    def drawPad(self):
        central_conductor = self.lib.new_cell(str("Central conductor "+ self.pad1))
        bondpad = gdspy.Rectangle([0,-self.width_pad/2],[self.length_pad, self.width_pad/2])
        path_to_waveguide = gdspy.Path(self.width_pad, initial_point = [self.length_pad, 0])
        path_to_waveguide.segment(self.pad_tail, direction = "+x", final_width = self.width_waveguide)
        
        central_conductor.add(bondpad)
        central_conductor.add(path_to_waveguide)
        
        gnd_pad = self.lib.new_cell(str("Ground "+ self.pad1))
        gnd_bondpad = gdspy.Rectangle([-self.gnd_offset_pad, -self.width_pad/2 - self.gnd_offset_pad],[self.length_pad, self.width_pad/2 + self.gnd_offset_pad])
        gnd_path_to_waveguide = gdspy.Path(self.width_pad + 2*self.gnd_offset_pad, initial_point = [self.length_pad, 0])
        gnd_path_to_waveguide.segment(self.pad_tail, direction = "+x", final_width = self.width_waveguide + 2*self.gnd_offset_waveguide)
        
        gnd_pad.add(gnd_bondpad)
        gnd_pad.add(gnd_path_to_waveguide)
        
        # cell = lib.new_cell("testCell")
        
        neg = gdspy.boolean(gnd_pad, central_conductor, "not")
        pos = gdspy.boolean(central_conductor, gnd_pad, "not")

        
        self.cell.add(neg)
        
        bd = self.cell.get_bounding_box()
        print(bd)
    
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)