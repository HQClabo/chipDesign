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
        
        self.layer = 3
        
        self.cell = self.lib.new_cell("Lumped element resonator")
        self.ghost = self.lib.new_cell("Ghost")
        
        #Set initial parameters
        self.length_inductor = 180
        self.spacing_inductor = 5
        self.width_inductor = 0.4
        self.width_resonator = 32.572
        self.width_capa_arm = 1.715
        self.length_capa_arm = 40
        self.height_capa_head = 10
        self.centre = coord_x, coord_y
        
    
    # def set_parameters(self, length_inductor, spacing_inductor, width_inductor, width_resonator, width_capa_arm, length_capa_arm,)
        
    
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
        if port == False:
            path = gdspy.FlexPath(M, self.width_inductor, layer = self.layer)
            self.cell.add(path)
            self.cell.add(head_capa)
            self.cell.add(arm1)
            self.cell.add(arm2)
            return self.cell
        else:
            path = gdspy.FlexPath(M[:-1], self.width_inductor, layer = self.layer)
            self.ghost.add(path)
            self.ghost.add(head_capa)
            self.ghost.add(arm1)
            self.ghost.add(arm2)
            return self.ghost
        
        
        
        
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
        print(res1_bb)
        
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
        
        

# test = lumped_element_resonator(0, 0)
# test.draw_resonator()
# print(test.get_bounding_box())



# # # gdspy.LayoutViewer()

# #quick tests cell reference
# bubu = gdspy.CellReference(test.draw_resonator()).translate(60, 60)

# lib = gdspy.GdsLibrary()
# newCell = lib.new_cell("test")

# # newCell.add(bubu)

# sv = 20
# sw = 10
# ground = 2.5
# headSpa = 5


# # bb = test.get_bounding_box()
# # rectv = gdspy.Rectangle([bb[0][0] - sw/2 + ground/2,bb[0][1] - headSpa], [bb[1][0] + sv/2 - ground/2, bb[1][1]])
# # rectw = gdspy.Rectangle([bb[0][0] - sv/2 + ground/2,bb[0][1] - headSpa], [bb[1][0] + sw/2 - ground/2, bb[1][1]])

# # rectangleCell = lib.new_cell("rectab")
# # rectangleCell.add(rectv)
# # rectCell2 = lib.new_cell("recta2")
# # rectCell2.add(rectw)

# # cellout = gdspy.CellReference(test.draw_resonator())


# # res1 = gdspy.Cell("res1")
# # testbool = gdspy.boolean(gdspy.CellReference(rectangleCell),cellout, "not")
# # res1.add(testbool)
# # bb = res1.get_bounding_box()

# # testbool2 = gdspy.CellReference(res1).translate(bb[1][0]-bb[0][0] + ground,0)
# # res2 = gdspy.Cell("res2")
# # res2.add(testbool2)
# # # newCell.add(test.draw_resonator())
# # # newCell.flatten()

# # cellArrayTest = lib.new_cell("array test")
# # # ArrayTest = gdspy.CellArray(newCell, 10, 10,(100,100))
# # # cellArrayTest.add(ArrayTest)
# # cellArrayTest.add(res1)
# # cellArrayTest.add(res2)
# # cellArrayTest.flatten()

# # testbool2 = gdspy.CellArray(testbool,1, 5, 5)


# uniMM = unidimensional_metamaterial(0, 0, 0, test.draw_resonator(), test.draw_resonator(port = True))
# # uniMM.layer = 5
# # uniMM.set_unit_cell()
# # uniMM.set_metamat_parameters(3, 20, 30, 30)
# uniMM.intercell_spacing = sv
# uniMM.intracell_spacing = sw
# uniMM.ground_spacing = ground
# uniMM.draw_metamaterial(4)

# uniMM.add_port()
# test = uniMM.output_metamaterial()
# # Utility.change_layer_of_entire_cell(test, 3, datatype=None)
# lib.add(test)
# # lib.add(uniMM.draw_metamaterial(3))

# lib.write_gds("test.gds")

# gdspy.LayoutViewer()
























