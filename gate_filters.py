# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 11:34:08 2022

@author: fopplige
"""

import numpy as np
import gdspy


class Pad:
    
    def __init__(self, cell, coord_x=0, coord_y=0, rotation=0):
        self.cell = cell
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
    
    def set_parameters(self, pad_size):
        self.pad_size = pad_size
    
    def draw_pad(self):
        self.cell.add(gdspy.Rectangle((-self.pad_size/2,-self.pad_size/2), (self.pad_size/2,self.pad_size/2)))


class InductorSpiral:
    
    def __init__(self, cell, coord_x=0, coord_y=0, rotation=0, ):
        self.cell = cell
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.inductance = 0
        self.length = 0
        
    def set_parameters(self, target_inductance, pad_size, ind_width, ind_gap, radius, tail):
        self.target_ind = target_inductance
        self.pad_size = pad_size
        self.ind_width = ind_width
        self.ind_gap = ind_gap
        self.radius = radius
        self.tail = tail

    def draw_inductor(self):
        ii=1
        d_in = self.pad_size + 2*self.ind_gap + self.ind_width
        ind_cal = self.get_inductance_square_spiral(1, d_in, d_in)
        while ind_cal < self.target_ind:
            ii += 1
            d_out = self.pad_size + 2*ii*(self.ind_gap + self.ind_width) - self.ind_width
            ind_cal = self.get_inductance_square_spiral(ii, d_in, d_out)

        spiral = self.draw_rectSpir(ii,self.pad_size,self.ind_width,self.ind_gap,self.radius,self.tail)
        self.cell.add(gdspy.boolean(spiral, None, 'or', max_points=0))
        self.inductance = self.get_inductance_square_spiral(ii, d_in, d_out)
        self.length = spiral.length

    def get_inductance_square_spiral(self,nTurns,d_in,d_out):
        # use dimesions in um
        k1 = 2.34
        k2 = 2.75
        d_avg = (d_out+d_in)/2
        inductance = k1*np.pi*4e-7*nTurns**2*d_avg*1e-6/(1+k2*d_out/d_in)
        return inductance

    def draw_rectSpir(self,nTurns,pad_size,width,delta,radius,tail):
        path = gdspy.Path(width,(-pad_size/2+width/2,pad_size/2))
        
        path.segment(delta+width/2-radius,'+y')
        for ii in range(2*nTurns):
            path.turn(radius,'r')
            path.segment(pad_size + (delta+width)*(ii+1) - width - 2*radius)
            path.turn(radius,'r')
            path.segment(pad_size + (delta+width)*(ii+1) + delta - 2*radius)
            
        path.turn(radius,'r')
        path.segment(pad_size/2 - 2*radius + (delta+width)*nTurns - width/2)
        path.turn(radius,'l')
        path.segment(tail)
        return path


class InductorMeander:
    
    def __init__(self, cell, coord_x=0, coord_y=0, rotation=0, ):
        self.cell = cell
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell
        self.inductance = 0
        self.length = 0

    def set_parameters(self, target_inductance, width_meander, width_wire, separation, tail):
        self.target_ind = target_inductance
        self.meander_width = width_meander
        self.ind_width = width_wire
        self.ind_gap = separation
        self.tail = tail
        self.sep = self.ind_gap+self.ind_width
    
    def draw_inductor(self):
        ii=2
        ind_cal = self.get_inductance_monomial(ii,self.meander_width,self.ind_width,self.ind_gap,self.tail)
        while ind_cal < self.target_ind:
            ii += 1
            self.length = ii * (self.meander_width + self.ind_gap) + 2*self.tail
            ind_cal = self.get_inductance_monomial(ii,self.meander_width,self.ind_width,self.ind_gap,self.tail)
        
        self.inductance = self.get_inductance_monomial(ii,self.meander_width,self.ind_width,self.sep,self.tail)
        self.length = ii * (self.meander_width + self.sep) + 2*self.tail
        meander = self.draw_meander(ii)
        self.cell.add(meander)

    def draw_meander(self,nTurns):
        path = gdspy.FlexPath([(0,0)],self.ind_width)

        half_width = self.meander_width/2 - self.ind_width/2
        
        path.segment((0,self.tail))
        for ii in range(nTurns-1):
            path.segment((-(-1)**ii*half_width,(ii)*self.sep+self.tail))
            path.segment((-(-1)**ii*half_width,(ii+1)*self.sep+self.tail))
            path.segment((0,(ii+1)*self.sep+self.tail))
        path.segment((0,ii*self.sep+2*self.tail))
        path.transform((self.coord_x,self.coord_y),self.rotation,1,False)
        
        return gdspy.boolean(path, None, 'or', max_points=0)

    def get_inductance_monomial(self,nTurns,width_meander,width_wire,separation,tail):
        inductance = 1e-9*(2.66 * (1e-3*tail)**0.0603 * (1e-3*width_meander)**0.4429 * (nTurns-1)**0.954
                      * (1e-3*separation)**0.606 * (1e-3*width_wire)**-0.173)
        return inductance


class Capacitor:

    def __init__(self, cell, coord_x=0, coord_y=0, rotation=0):
        self.cell = cell
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.rotation = rotation
        self.cell = cell

    def set_parameters(self,n_bars,length_bar=10,width_bar=1,width_line=1,separation=1,tail=10):
        self.n_bars = n_bars
        self.length_bar = length_bar
        self.width_bar = width_bar
        self.width_line = width_line
        self.sep = separation
        self.tail = tail
        
    def draw_capacitor(self):
        cell_bars = gdspy.Cell('bar')
        
        length = self.n_bars*(self.width_bar + self.sep) - self.sep + 2*self.tail
        line = gdspy.Path(self.width_line,(0,0))
        line.segment(length,'+y')
        
        bar = gdspy.Rectangle((-self.length_bar/2,-self.width_bar/2), (self.length_bar/2,self.width_bar/2))
        cell_bars.add(bar)
        array = gdspy.CellArray(cell_bars, 1, self.n_bars, (0, self.sep+self.width_bar), origin=(0, self.tail))
        
        self.cell.add(gdspy.boolean(line,array,'or',max_points=0))
        gdspy.current_library.remove('bar')
