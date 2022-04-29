# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 11:30:27 2022

@author: sbroggio
"""

import gdspy
import chipDesign.Utility as Utility
# from chipDesign.SQUID_array import squid_array

class WaveguideArrayHole:
    
    def __init__(self, coord_x, coord_y, rotation):
        lib = gdspy.GdsLibrary()
        gdspy.current_library = lib
        
        cell = lib.new_cell("WaveguideArrayHole")
        SQUID_slots = lib.new_cell("SQUID_slots")
        CelllowerWaveguidePath = lib.new_cell("CelllowerWaveguidePath")
        cellOffset = lib.new_cell("cellOffset")      
        cellupperWaveguidePath = lib.new_cell("cellupperWaveguidePath")
        merged = lib.new_cell("Merged")       
        cellrectangleForLowerHole = lib.new_cell("cellrectangleForLowerHole")
        cellpatchRectangle = lib.new_cell("cellpatchRectangle")
        cellPad = lib.new_cell("Pads")
        testArray = lib.new_cell("TetsArray")
        
        
        squid = lib.new_cell("cellpatchRectangleaaaaaa")
        
        
        
        
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.lib = lib
        self.SQUID_slots = SQUID_slots
        self.CelllowerWaveguidePath = CelllowerWaveguidePath
        self.cellOffset = cellOffset
        self.merged = merged
        self.cellrectangleForLowerHole = cellrectangleForLowerHole
        self.cellpatchRectangle = cellpatchRectangle
        self.cellupperWaveguidePath = cellupperWaveguidePath
        self.cellPad = cellPad
        self.testArray = testArray
        
        
        self.squid = squid
        
    def setParameters(self, width, spacing, length, radius, initLength): #set waveguide parameters
        self.length = length
        self.radius = radius
        self.initLength = initLength
        self.width = width
        self.spacing = spacing
    
    def setHolesParameters(self, slotNumber, slotWidth, slotHeigth, bottomspacing, horizontalSpacing): #set slots parameters
        self.slotNumber = slotNumber
        self.slotWidth = slotWidth
        self.slotHeigth = slotHeigth
        self.bottomspacing = bottomspacing
        self.horizontalSpacing = horizontalSpacing
        
        
    def drawWaveguide(self):
        # draw main waveguide
        waveguidePath = gdspy.Path(self.width, (0, 300), number_of_paths=2, distance = self.spacing + self.width)
        # waveguidePath.segment(self.initLength - 10, "+y")
        # waveguidePath.turn(self.radius - 10, "r")
        waveguidePath.segment(self.length, "+x")
        # waveguidePath.turn(self.radius - 10, "r")
        # waveguidePath.segment(self.initLength - 10, "-y")
        
        # SQUID slots insertion
        SQUID_slot = gdspy.Rectangle((-self.slotWidth/2,0), (self.slotWidth/2,self.slotHeigth))
        self.SQUID_slots.add(SQUID_slot)
        
        # lower waveguide connection
        lowerWaveguidePath = gdspy.Path(self.slotWidth/2,(0,10))
        lowerWaveguidePath.segment(100,"+y",final_width=self.slotWidth/4)
        lowerWaveguidePath.turn(40, 'l',final_width=self.slotWidth/8)
        lowerWaveguidePath.segment(30,"-x",final_width=self.slotWidth/20)
        lowerWaveguidePath.turn(10,'r',final_width=self.slotWidth/20)
        lowerWaveguidePath.segment(80,"+y")
        self.CelllowerWaveguidePath.add(lowerWaveguidePath)
        
        
        
        #offset
        self.cellOffset.add(gdspy.offset(gdspy.boolean(lowerWaveguidePath,None,"or",max_points=0), 2))
        
        
        #adjusting offset
        rectangleForLowerHole = gdspy.Rectangle((self.radius + self.horizontalSpacing - self.slotWidth/4,self.radius + self.width/2 + self.spacing/8-1), (self.radius + self.horizontalSpacing - self.slotWidth/4 + self.slotWidth/2,self.radius + self.width/2 + self.spacing/8 + 10))
        self.cellrectangleForLowerHole.add(rectangleForLowerHole)
        arrayLowerRectangle = gdspy.CellArray(self.cellrectangleForLowerHole, self.slotNumber -1, 1, [self.length/(self.slotNumber-1),0])
        
        
        # upper waveguide connection
        upperWaveguidePath = gdspy.Path(5,(-55,-5))
        upperWaveguidePath.segment(230,"+y")
        upperWaveguidePath.turn(0, 'l')
        upperWaveguidePath.segment(20,"-x")
        upperWaveguidePath.turn(0,'r')
        upperWaveguidePath.segment(50,"+y")
        self.cellupperWaveguidePath.add(upperWaveguidePath)
        Utility.change_layer_of_entire_cell(self.cellupperWaveguidePath, 2)
        
        
        
        
        #patching parameters
        patchRectangle = gdspy.Rectangle((self.radius + self.horizontalSpacing - self.slotWidth/4 + self.slotWidth/3 + 50 ,self.radius + self.width/2 + self.spacing/8-1-20), (self.radius + self.horizontalSpacing - self.slotWidth/4 + 1.2*self.slotWidth + 86, self.radius + self.width/2 + self.spacing/8 ), layer = 2)     
        patchRectangle2 = gdspy.Rectangle((self.radius + self.horizontalSpacing - self.slotWidth/4 + self.slotWidth/3 -100,self.radius + self.width/2 + self.spacing/8-1-20), (self.radius - self.slotWidth/4 + 1.2*self.slotWidth + 70 , self.radius + self.width/2 + self.spacing/8 + 100), layer = 2)     
        patchRectangle3 = gdspy.Rectangle((self.radius + self.horizontalSpacing - self.slotWidth/4 + self.slotWidth/3 + 60,self.radius + self.width/2 + self.spacing/8 + 13), (self.radius + self.horizontalSpacing - self.slotWidth/4 + 1.2*self.slotWidth + 30, self.radius + self.width/2 + self.spacing/8 + 18), layer = 2)     
        
        patchRectangle4 = gdspy.Rectangle((self.radius + self.horizontalSpacing - self.slotWidth/4 + self.slotWidth/3 -50 + 222,self.radius + self.width/2 + self.spacing/8-1-110), (self.radius - self.slotWidth/4 + 1.2*self.slotWidth + 300 , self.radius + self.width/2 + self.spacing/8 -80), layer = 2)     
        # self.cellpatchRectangle.add(patchRectangle)
        # self.cellpatchRectangle.add(patchRectangle2)
        # arrayPatching = gdspy.CellArray(self.cellpatchRectangle, self.slotNumber -1, 1, [self.length/(self.slotNumber-1),0],origin=(-2*self.slotWidth,self.bottomspacing + self.spacing - self.slotHeigth/16))
        # self.cell.add(arrayPatching)
        
        
        
        if self.rotation == 0: 
            #create array of SQUID array
            #create array of lower path
            #create array of lower path with offset
            SQUIDslotArray = gdspy.CellArray(self.SQUID_slots, self.slotNumber - 1, 1, [self.length/(self.slotNumber-1),0],(self.radius,self.radius + (self.spacing+self.width)/2 + self.width/2 + self.bottomspacing))
            lowerPathArray = gdspy.CellArray(self.CelllowerWaveguidePath, self.slotNumber - 1, 1, [self.length/(self.slotNumber-1),0],(self.radius + self.horizontalSpacing ,self.radius + (self.spacing+self.width)/2 - self.width/2))
            OffsetlowerPathArray = gdspy.CellArray(self.cellOffset, self.slotNumber - 1, 1, [self.length/(self.slotNumber-1),0],(self.radius + self.horizontalSpacing ,self.radius + (self.spacing+self.width)/2 - self.width/2))
            
            
            #merge everything in a single cell exept "lowerPathArray" which has to be subtracted
            self.merged.add(SQUIDslotArray)
            self.merged.add(OffsetlowerPathArray)
            self.merged.add(waveguidePath)
            
            
            #patching instantiation
            self.cellpatchRectangle.add(patchRectangle)
            self.cellpatchRectangle.add(patchRectangle2)
            arrayPatching = gdspy.CellArray(self.cellpatchRectangle, self.slotNumber -1, 1, [self.length/(self.slotNumber-1),0],origin=(-2*self.slotWidth,self.bottomspacing + self.spacing - self.slotHeigth/16))
            self.cell.add(arrayPatching)
            

            
            
            # subract "lowerPathArray"
            booleanWaveguide = gdspy.boolean(self.merged, lowerPathArray, 'not')
            
            # subtract array of rectangle for offset correction 
            booleanWaveguide2 = gdspy.boolean(booleanWaveguide, arrayLowerRectangle, 'not')           
            self.cell.add(booleanWaveguide2)
            
            
            pads = gdspy.Rectangle((-50,-50), (50,50))  
            self.cellPad.add(pads)
            padsarray = gdspy.CellArray(self.cellPad, 8, 2, [200,300], origin= (2000,1150))
            self.cell.add(padsarray)
            
            
            # SQUIDArray = squid_array(38,0,0,0)
            # self.testArray.add(SQUIDArray.draw_squid_array())
            # testarray = gdspy.CellArray(self.testArray, 8, 1, [200,400], origin= (2000,1200))
            # self.cell.add(testarray)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        else:
            
            #create array of SQUID array
            #create array of upper path
            SQUIDslotArray = gdspy.CellArray(self.SQUID_slots, self.slotNumber -1 , 1, [self.length/(self.slotNumber-1),0],(self.radius,self.radius + (self.spacing+self.width)/2 + self.width/2))
            upperPathArray = gdspy.CellArray(self.cellupperWaveguidePath, self.slotNumber - 1, 1, [self.length/(self.slotNumber-1),0],(self.radius + self.horizontalSpacing ,self.radius + (self.spacing+self.width)/2 - self.width/2))
            
            
            self.cell.add(waveguidePath)
            self.cell.add(SQUIDslotArray)
            self.cell.add(upperPathArray)
                 
            #patching instantiation
            
            self.cellpatchRectangle.add(patchRectangle2)
            self.cellpatchRectangle.add(patchRectangle3)
            self.cellpatchRectangle.add(patchRectangle4)
            arrayPatching = gdspy.CellArray(self.cellpatchRectangle, self.slotNumber -1, 1, [self.length/(self.slotNumber-1),0],origin=(-2*self.slotWidth,self.bottomspacing + self.spacing - self.slotHeigth/16))
            
            
            
            self.cell.add(arrayPatching)
        
        return Utility.rotation(self.cell, self.coord_x, self.coord_y, self.rotation)
    
    
    def drawArray(self, SQUID_Array): #draw Array of SQUID_Array
    
        # singleArray = SQUID_Array
        if self.rotation == 0:    
            SQUIDmultiple = gdspy.CellArray(SQUID_Array, self.slotNumber -1 , 1, [self.length/(self.slotNumber-1),0],(self.radius,self.radius + (self.spacing+self.width)/2 + self.width/2 + self.bottomspacing + self.slotHeigth/8))
            self.squid.add(SQUIDmultiple)
        else:
            SQUIDmultiple = gdspy.CellArray(SQUID_Array, self.slotNumber - 1, 1, [self.length/(self.slotNumber-1),0],(self.radius,self.radius + (self.spacing+self.width)/2 + self.width/2 + self.slotHeigth/8 ))
            self.squid.add(SQUIDmultiple)        
        
        return Utility.rotation(self.squid, self.coord_x, self.coord_y, self.rotation)
