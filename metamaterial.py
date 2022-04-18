# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 23:41:07 2022

@author: sbroggio
"""

import gdspy
import Utility

#to be rearranged

class metamaterial:
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
        



class lumped_element_resonator:
    def __init__(self,coord_x, coord_y):
        self.lib = gdspy.GdsLibrary()
        gdspy.current_library = self.lib
        
        self.cell = self.lib.new_cell("Lumped element resonator")
        
        #Set initial parameters
        self.length_inductor = 1000
        self.spacing_inductor = 3
        self.width_inductor = 0.5
        self.width_resonator = 60
        self.width_capa_arm = 3
        self.length_capa_arm = 40
        self.height_capa_head = 10
        self.centre = coord_x, coord_y
        
    
        
    
    def draw_resonator(self, port = False):
        #A = width_resonator
        #L = length_inductor
        #t = width_capa_arm
        #s = spacing_inductor
        #w = width_inductor
        #calculate horizontal dimension of inductor
        b = 3/5*self.width_resonator - 2*self.width_capa_arm
        #print('b: ',b)
        
        #calculate number of windings   
        N = int((self.length_inductor-2*(self.spacing_inductor+self.width_inductor))/(b+self.spacing_inductor))
        
        #adapt start & end segment of inductor
        d_prime = 0.5*(self.length_inductor - N*(self.spacing_inductor + b)) + self.width_inductor
        #print('d_prime: ',d_prime)
        
        #calculate vertical dimension of capacitor
        # B = N*(self.spacing_inductor+self.width_inductor) + d_prime + self.height_capa_head
        # print('B: ', B)
        
        #Ushape, we take the centre at at the bottom/top of the U
        head_capa_points = [self.centre[0] - self.width_resonator/2, self.centre[1] - self.height_capa_head], [self.centre[0] + self.width_resonator/2, self.centre[1]]
        head_capa = gdspy.Rectangle(head_capa_points[0], head_capa_points[1])
        
        arm1_points = [self.centre[0] - self.width_resonator/2, self.centre[1]], [self.centre[0] - self.width_resonator/2 + self.width_capa_arm, self.centre[1] + self.length_capa_arm]
        arm2_points = [self.centre[0] + self.width_resonator/2 - self.width_capa_arm, self.centre[1]], [self.centre[0] + self.width_resonator/2, self.centre[1] + self.length_capa_arm]
        arm1 = gdspy.Rectangle(arm1_points[0], arm1_points[1])
        arm2 = gdspy.Rectangle(arm2_points[0], arm2_points[1])
        
        self.cell.add(head_capa)
        self.cell.add(arm1)
        self.cell.add(arm2)
        
        
        M = []
        v0,w0 = self.centre[0], self.centre[1]
        M.append([v0,w0])
        v1,w1 = v0, w0 + d_prime - self.width_inductor/2
        M.append([v1,w1])
        
        for i in range(N):
            if i%2 == 0:
                v2, w2 = M[-1][0] - b/2 + self.width_inductor/2, M[-1][1]
                M.append([v2,w2])
                v3, w3 = v2, w2 + (self.spacing_inductor+self.width_inductor)
                M.append([v3,w3])
                v4, w4 = v3 + (b/2 - self.width_inductor/2), w3
                M.append([v4,w4])
                # print(i)
            if (i+1)%2==0:
                v5,w5 = M[-1][0] + b/2 - self.width_inductor/2, M[-1][1]
                M.append([v5,w5])
                v6, w6 = v5, w5 + (self.spacing_inductor+self.width_inductor)
                M.append([v6,w6])
                v7,w7 = v6 - b/2 + self.width_inductor/2, w6
                M.append([v7,w7])
                # print(i)
            if (i+1)==N:
                # print('end turns:', M[-1])
                v8,w8 = M[-1][0], M[-1][1]
                v9, w9 = v8, w8 + d_prime - self.width_inductor/2
                M.append([v9,w9])
                # print('end meander:', M[-1])
            # else:
                # print('not entered')
        if port == False:
            path = gdspy.FlexPath(M, self.width_inductor)
        else:
            path = gdspy.FlexPath(M[:-1], self.width_inductor)
        
        self.cell.add(path)
        return self.cell
        
        
    def get_bounding_box(self):
        return self.cell.get_bounding_box()


class unidimensional_metamaterial:
    #For the moment only possible to implement dimers
    def __init__(self, n_unit_cell, N_unit_cell, resonator_cell):
        self.lib = gdspy.GdsLibrary()
        gdspy.current_library = self.lib
        
        self.resonator_cell = resonator_cell
        self.cell = self.lib.new_cell("Metamaterial")
        self.unit_cell = self.lib.new_cell("Unit cell")
        self.rect1Cell = self.lib.new_cell("Box1")
        self.rect2Cell = self.lib.new_cell("Box2")
        # self.res1 = self.lib.new_cell("res1")
        # self.res2 = self.lib.new_cell("res2")
        self.res1neg = self.lib.new_cell("Negative resonator 1")
        self.res2neg = self.lib.new_cell("Negative resonator 2")
        
        
        self.N_unit_cell = N_unit_cell
        self.n_unit_cell = n_unit_cell
        self.head_spacing_to_GND = 3
        self.ground_spacing = 3
        
        self.intercell_spacing = 10
        self.intracell_spacing = 30
        
    
    def set_parameters(self,head_spacing_to_GND, ground_spacing, intercell_spacing, intracell_spacing):
        self.head_spacing_to_GND = head_spacing_to_GND
        self.ground_spacing = ground_spacing
        self.intercell_spacing = intercell_spacing
        self.intracell_spacing = intracell_spacing
    
    
    def set_unit_cell(self):
        
        resonator_box = self.resonator_cell.get_bounding_box()
        #Create box for first resonator
        
        rect1 = gdspy.Rectangle([resonator_box[0][0] - self.intracell_spacing/2 + self.ground_spacing/2,resonator_box[0][1] - self.head_spacing_to_GND], [resonator_box[1][0] + self.intercell_spacing/2 - self.ground_spacing/2, resonator_box[1][1]])
        self.rect1Cell.add(rect1)
        #Create box for first resonator
        rect2 = gdspy.Rectangle([resonator_box[0][0] - self.intercell_spacing/2 + self.ground_spacing/2,resonator_box[0][1] - self.head_spacing_to_GND], [resonator_box[1][0] + self.intracell_spacing/2 - self.ground_spacing/2, resonator_box[1][1]])
        self.rect2Cell.add(rect2)
        
        box_rectangle = self.rect2Cell.get_bounding_box()
        #Do negative of the two resonators
        neg1 = gdspy.boolean(gdspy.CellReference(self.rect1Cell), gdspy.CellReference(self.resonator_cell), "not")
        self.res1neg.add(neg1)
        neg2 = gdspy.boolean(gdspy.CellReference(self.rect2Cell), gdspy.CellReference(self.resonator_cell), "not").translate(box_rectangle[1][0] - box_rectangle[0][0] + self.ground_spacing - (self.intracell_spacing - self.intercell_spacing)/2, 0)
        self.res2neg.add(neg2)
        
        
        self.unit_cell.add(self.res1neg)
        self.unit_cell.add(self.res2neg)
        
        return self.unit_cell
    
    
    def draw_metamaterial(self):
        unit_cell = self.set_unit_cell()
        box_unit_cell = unit_cell.get_bounding_box()
        array = gdspy.CellArray(unit_cell, self.N_unit_cell, 1, (box_unit_cell[1][0] - box_unit_cell[0][0] + self.ground_spacing,0))
        self.cell.add(array)
        
        return self.cell.flatten()
    
    























