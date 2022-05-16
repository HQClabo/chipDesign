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
        
        self.layer = 0
        
        self.cell = self.lib.new_cell("Lumped element resonator")
        self.cell_neg = self.lib.new_cell("Lumped element resonator negative")
        self.ghost = self.lib.new_cell("Ghost")
        self.ghost_neg = self.lib.new_cell("Ghost negative")
        self.rectangle_for_negative = self.lib.new_cell("Rectangle for negative")
        
        #Set initial parameters
        self.length_inductor = 180
        self.spacing_inductor = 5
        self.width_inductor = 0.5
        self.width_resonator = 32.572
        self.width_capa_arm = 1.715
        self.length_capa_arm = 40
        self.height_capa_head = 10
        self.head_spacing_to_GND = 3
        self.centre = coord_x, coord_y
        
    
    # def set_parameters(self, length_inductor, spacing_inductor, width_inductor, width_resonator, width_capa_arm, length_capa_arm,)
        
    
    def draw_resonator(self, port = False):
        #A = width_resonator
        #L = length_inductor
        #t = width_capa_arm
        #s = spacing_inductor
        #w = width_inductor
        #calculate horizontal dimension of inductor
        b = 1/2*self.width_resonator - 2*self.width_capa_arm
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
        arm1 = gdspy.Rectangle(arm1_points[0], arm1_points[1], layer = self.layer)
        arm2 = gdspy.Rectangle(arm2_points[0], arm2_points[1], layer = self.layer)
        
        # self.cell.add(head_capa)
        # self.cell.add(arm1)
        # self.cell.add(arm2)
        
        
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
        # if port == False:1
        path = gdspy.FlexPath(M, self.width_inductor, layer = self.layer)
        self.cell.add(path)
        self.cell.add(head_capa)
        self.cell.add(arm1)
        self.cell.add(arm2)
        # return self.cell
        # else:
        path = gdspy.FlexPath(M[:-1], self.width_inductor, layer = self.layer)
        self.ghost.add(path)
        self.ghost.add(head_capa)
        self.ghost.add(arm1)
        self.ghost.add(arm2)
        # return self.ghost
        if port == False:
            return self.cell
        else:
            return self.ghost
        
        
    def make_resonator_negative(self, port = False):
        # self.rectangle_for_negative = self.lib.new_cell("Rectangle for negative")
        bb = self.cell.get_bounding_box()
        print(bb)
        self.rectangle_for_negative.add(gdspy.Rectangle((bb[0][0], bb[0][1]- self.head_spacing_to_GND),bb[1]))
        self.cell_neg.add(gdspy.boolean(gdspy.CellReference(self.rectangle_for_negative), gdspy.CellReference(self.cell), "not"))
        self.ghost_neg.add(gdspy.boolean(gdspy.CellReference(self.rectangle_for_negative), gdspy.CellReference(self.ghost), "not"))
        if port == False:
            return self.cell_neg
        else:
            return self.ghost_neg
        # return "test"
        
    def get_bounding_box(self):
        return self.cell.get_bounding_box()



class unidimensional_metamaterial:
    #For the moment only possible to implement dimers
    def __init__(self,coord_x, coord_y, rotation, resonator_cell, ghost):
        self.lib = gdspy.GdsLibrary()
        gdspy.current_library = self.lib
        
        self.layer = 3
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        
        self.ghost = ghost
        self.resonator_cell = resonator_cell
        self.cell = self.lib.new_cell("Metamaterial")
        self.unit_cell = self.lib.new_cell("Unit cell")
        self.rect1Cell = self.lib.new_cell("Box1")
        self.rect2Cell = self.lib.new_cell("Box2")
        
        self.testCell = self.lib.new_cell("testcell")
        self.testCell2 = self.lib.new_cell("testcell2")
        self.portLeft = self.lib.new_cell("PortLeft")
        self.portRight = self.lib.new_cell("PortRight")
        # self.res1 = self.lib.new_cell("res1")
        # self.res2 = self.lib.new_cell("res2")
        self.res1neg = self.lib.new_cell("Negative resonator 1")
        self.res2neg = self.lib.new_cell("Negative resonator 2")
        
        
        
        # self.N_unit_cell = N_unit_cell
        self.head_spacing_to_GND = 3
        self.ground_spacing = 2
        
        # self.intercell_spacing = 15
        # self.intracell_spacing = 15
        
        self.spacings = [20,10]
        
        
        self.width_WG_end = 5
        self.length_WG = 40
        self.width_WG = 21
        
        
    
    def __set_unit_cell(self):
        #idea: Using the rectangle cell for each side of the resonators
        #With a for loop you can make generate the new cells.
        res_bb = self.resonator_cell.get_bounding_box()
        width_resonator = res_bb[1][0] - res_bb[0][0]
        # print(res_bb)
        # print(width_resonatpor)
        # cell_bb = [[0,0],[0,0]]
        dis = 0
        cumulSpace = 0
        for k, i in enumerate(self.spacings):
            
            # print(i)
            #create cells for rectangles
            rectangle_left_cell = self.lib.new_cell("Left rectangle")
            # rectangle_right_cell = self.lib.new_cell("Right rectangle")
            
            #create rectangles
            rectangle_left = gdspy.Rectangle([res_bb[0][0],res_bb[0][1]], [res_bb[0][0] - (self.spacings[k-1])/2 + self.ground_spacing/2,res_bb[1][1]])
            rectangle_right = gdspy.Rectangle([res_bb[1][0],res_bb[0][1]], [res_bb[1][0] + (self.spacings[k])/2 - self.ground_spacing/2,res_bb[1][1]])
            
            rectangle_left_cell.add(rectangle_left)
            rectangle_left_cell.add(rectangle_right)
            self.testCell2.add(gdspy.boolean(gdspy.CellReference(self.resonator_cell).translate(dis, 0), gdspy.CellReference(rectangle_left_cell).translate(dis, 0), "or"))
            # cell_bb = self.testCell2.get_bounding_box()
            # dis = cell_bb[1][0]-cell_bb[0][0]
            cumulSpace += i
            dis = (k+1)*(width_resonator) + cumulSpace
            # print(cell_bb)
            self.lib.remove("Left rectangle")
            
            # self.lib.remove("test")
        
        return self.testCell2
    
    
    def draw_metamaterial(self,N_unit_cell):
        unit_cell = self.__set_unit_cell()
        box_unit_cell = unit_cell.get_bounding_box()
        array = gdspy.CellArray(unit_cell, N_unit_cell, 1, (box_unit_cell[1][0] - box_unit_cell[0][0] + self.ground_spacing,0))
        self.cell.add(array)
    
    
    def add_port(self):
        #takes the last spacing for the space to the right
        metamat_bb = self.cell.get_bounding_box()
        resonator_bb = self.resonator_cell.get_bounding_box()
        ghost_bb = self.ghost.get_bounding_box()
        width_resonator = resonator_bb[1][0] - resonator_bb[0][0]
        left_coord = [ghost_bb[0][0],(ghost_bb[1][1]+ghost_bb[0][1])/2]
        right_coord = [ghost_bb[1][0],(ghost_bb[1][1]+ghost_bb[0][1])/2]
        rectGhostCellLeft = self.lib.new_cell("GhostCellLeft")
        rectGhostCellRight = self.lib.new_cell("GhostCellRight")
        
        
        #Left port
        rectangleLeftLeft = gdspy.Rectangle(ghost_bb[0],[ghost_bb[0][0]-width_resonator,ghost_bb[1][1]])
        rectangleRightLeft = gdspy.Rectangle([ghost_bb[1][0],ghost_bb[0][1]],[ghost_bb[1][0] + self.spacings[-1]/2 - self.ground_spacing/2,ghost_bb[1][1]])
        
        left_wg = gdspy.Path(self.width_WG_end, initial_point=left_coord)
        left_wg.segment(width_resonator,direction = "-x", final_width= self.width_WG)
        rectGhostCellLeft.add(gdspy.boolean(rectangleLeftLeft,left_wg,"not"))
        rectGhostCellLeft.add(rectangleRightLeft)
        rectGhostCellLeft.add(self.ghost)
        
        #Right port
        rectangleLeftRight = gdspy.Rectangle(ghost_bb[0],[ghost_bb[0][0] - self.spacings[-1]/2 + self.ground_spacing/2,ghost_bb[1][1]])
        rectangleRightRight = gdspy.Rectangle([ghost_bb[1][0],ghost_bb[0][1]],[ghost_bb[1][0] + width_resonator,ghost_bb[1][1]])
        
        right_wg = gdspy.Path(self.width_WG_end, initial_point=right_coord)
        right_wg.segment(width_resonator,direction = "+x", final_width= self.width_WG)
        
        # rectGhost1CellRight.add(right_wg)
        # rectGhostCellRight.add(rectangleRight)
        
        rectGhostCellRight.add(gdspy.boolean(rectangleRightRight,right_wg,"not"))
        rectGhostCellRight.add(rectangleLeftRight)
        rectGhostCellRight.add(self.ghost)
        
        
        
        self.cell.add(gdspy.CellReference(rectGhostCellLeft, origin = (-width_resonator-self.spacings[-1],0)))
        self.cell.add(gdspy.CellReference(rectGhostCellRight,origin = (metamat_bb[1][0]+width_resonator/2 + self.spacings[-1]/2 + self.ground_spacing/2,0)))
        
        
        
        
        
    def output_metamaterial(self):
        print(self.layer)
        Utility.change_layer_of_entire_cell(self.cell, 3)
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        # metamaterial_bounding_box = self.cell.get_bounding_box()
        
    def get_coord(self):
        return self.left_wgCoord, self.right_wgCoord
        
        


class unidimensional_metamaterial_OLD:
    #For the moment only possible to implement dimers
    def __init__(self,coord_x, coord_y, rotation, resonator_cell, ghost):
        self.lib = gdspy.GdsLibrary()
        gdspy.current_library = self.lib
        
        self.layer = 3
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        
        self.ghost = ghost
        self.resonator_cell = resonator_cell
        self.cell = self.lib.new_cell("Metamaterial")
        self.unit_cell = self.lib.new_cell("Unit cell")
        self.rect1Cell = self.lib.new_cell("Box1")
        self.rect2Cell = self.lib.new_cell("Box2")
        self.rectGhostCellLeft = self.lib.new_cell("GhostCellLeft")
        self.rectGhostCellRight = self.lib.new_cell("GhostCellRight")
        self.testCell = self.lib.new_cell("testcell")
        self.testCell2 = self.lib.new_cell("testcell2")
        self.portLeft = self.lib.new_cell("PortLeft")
        self.portRight = self.lib.new_cell("PortRight")
        # self.res1 = self.lib.new_cell("res1")
        # self.res2 = self.lib.new_cell("res2")
        self.res1neg = self.lib.new_cell("Negative resonator 1")
        self.res2neg = self.lib.new_cell("Negative resonator 2")
        
        
        
        # self.N_unit_cell = N_unit_cell
        self.head_spacing_to_GND = 3
        self.ground_spacing = 2.5
        
        self.intercell_spacing = 15
        self.intracell_spacing = 15
        
        
        
        self.width_WG_end = 5
        self.length_WG = 40
        self.width_WG = 21
        
    
    # def set_WG_parameters(self, width_WG, length_WG, width_WG_end):
    #     self.width_WG = width_WG
    #     self.length_WG = length_WG
    #     self.width_WG_end = width_WG_end
    
    # def set_metamat_parameters(self, head_spacing_to_GND, ground_spacing, intercell_spacing, intracell_spacing):
    #     self.head_spacing_to_GND = head_spacing_to_GND
    #     self.ground_spacing = ground_spacing
    #     self.intercell_spacing = intercell_spacing
    #     self.intracell_spacing = intracell_spacing

        
    
    
    def __set_unit_cell(self):
        
        resonator_box = self.resonator_cell.get_bounding_box()
        #Create box for first resonator
        
        rect1 = gdspy.Rectangle([resonator_box[0][0] - self.intracell_spacing/2 + self.ground_spacing/2,resonator_box[0][1] - self.head_spacing_to_GND], [resonator_box[1][0] + self.intercell_spacing/2 - self.ground_spacing/2, resonator_box[1][1]],layer = self.layer)
        self.rect1Cell.add(rect1)
        #Create box for first resonator
        rect2 = gdspy.Rectangle([resonator_box[0][0] - self.intercell_spacing/2 + self.ground_spacing/2,resonator_box[0][1] - self.head_spacing_to_GND], [resonator_box[1][0] + self.intracell_spacing/2 - self.ground_spacing/2, resonator_box[1][1]], layer = self.layer)
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
    
    
    
    def draw_metamaterial(self,N_unit_cell):
        unit_cell = self.__set_unit_cell()
        box_unit_cell = unit_cell.get_bounding_box()
        array = gdspy.CellArray(unit_cell, N_unit_cell, 1, (box_unit_cell[1][0] - box_unit_cell[0][0] + self.ground_spacing,0))
        
        self.cell.add(array)
        # return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
        
    
    def add_port(self):
        #add waveguide connection
        ghost_bb = self.ghost.get_bounding_box()
        metamat_bb = self.cell.get_bounding_box()
        
        res1_bb = self.rect2Cell.get_bounding_box()
        res2_bb = self.rect1Cell.get_bounding_box()
        
        left_coord = [ghost_bb[0][0],(metamat_bb[1][1]+metamat_bb[0][1])/2]
        # print(left_coord)
        right_coord = [ghost_bb[1][0],(metamat_bb[1][1]+metamat_bb[0][1])/2]
        
        
        self.left_wgCoord = left_coord
        self.right_wgCoord = right_coord
        
        right_wg = gdspy.Path(self.width_WG_end,initial_point=right_coord)
        right_wg.segment(self.length_WG,direction = "+x", final_width= self.width_WG)
        
        left_wg = gdspy.Path(self.width_WG_end,initial_point=left_coord)
        left_wg.segment(self.length_WG,direction = "-x", final_width= self.width_WG)
        
        
        self.rectGhostCellLeft.add(self.ghost)
        self.rectGhostCellLeft.add(left_wg)
        
        self.rectGhostCellRight.add(self.ghost)
        self.rectGhostCellRight.add(right_wg)
        
        res1_bb = self.rect2Cell.get_bounding_box()
        # print(res1_bb)
        
        #VERY DODGY BELOW
        rect_left = gdspy.Rectangle([res1_bb[0][0] - self.length_WG + self.intracell_spacing + self.ground_spacing/2 ,res1_bb[0][1]], [res1_bb[1][0],res1_bb[1][1]])
        self.testCell.add(rect_left)
        neg_ghost_left = gdspy.boolean(gdspy.CellReference(self.testCell), gdspy.CellReference(self.rectGhostCellLeft), "not").translate(-(res1_bb[1][0]-metamat_bb[0][0] + self.ground_spacing),0)
        res2_bb = self.rect1Cell.get_bounding_box()
        rect_right = gdspy.Rectangle([res2_bb[0][0] ,res2_bb[0][1]], [res2_bb[1][0] + self.length_WG - self.intracell_spacing - self.ground_spacing/2,res2_bb[1][1]])
        
        self.testCell2.add(rect_right)
        neg_ghost_right = gdspy.boolean(gdspy.CellReference(self.testCell2), gdspy.CellReference(self.rectGhostCellRight), "not").translate(-(res2_bb[0][0]-metamat_bb[1][0] - self.ground_spacing),0)
        # return print(type(neg_ghost_left))
    
    
        self.portLeft.add(neg_ghost_left)
        self.portRight.add(neg_ghost_right)
        
        self.cell.add(self.portLeft)
        self.cell.add(self.portRight)
        
        
        # self.cell.add(Utility.rotation(self.portLeft, 0, 0, 0))
        
        
        
        
    def output_metamaterial(self):
        print(self.layer)
        Utility.change_layer_of_entire_cell(self.cell, 3)
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
        # metamaterial_bounding_box = self.cell.get_bounding_box()
        
    def get_coord(self):
        return self.left_wgCoord, self.right_wgCoord
        
        
        # rectleft_ghost = gdspy.Rectangle([], point2)
        



sv = 20
sw = 10
ground = 2.5
headSpa = 5

resonator = lumped_element_resonator(0, 0)
resonator_cell = resonator.draw_resonator()
negative_resonator = resonator.make_resonator_negative()
ghost = lumped_element_resonator(0, 0)
ghost_cell = ghost.draw_resonator(port = True)
negative_ghost = ghost.make_resonator_negative(port = True)

metamat = unidimensional_metamaterial(0, 0, 0, negative_resonator, negative_ghost)
metamat.spacings = [9,30]
# metamat.set_unit_cellv2()
metamat.draw_metamaterial(3)
metamat.add_port()



lib = gdspy.GdsLibrary()
lib.add(metamat.output_metamaterial())
lib.write_gds("testMetamat.gds")

gdspy.LayoutViewer()
























