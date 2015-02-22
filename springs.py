# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 12:43:10 2015

@author: Christopher R. Carlson, crcarlson@gmail.com

Spring property calculator as defined by: http://www.efunda.com/DesignStandards/springs/calc_comp_designer.cfm#calc
Other design notes:
    - Spring clearance: about 10 percent of the diameter (0.160 hole ==> 0.144 spring diameter)
    - Ideal spring index (ratio of diameter to wire size) is about 9
    - for 10x6 cycles, design for 50 percent of tensile strength
    - Springs are generally sized as a function of the energy they will store
    - The ratio of max_deflection/solid_height depends on the index (spring_diameter / wire_diameter)
    - The top 20 percent and bottom 20 percent of spring travel are where the spring will be more non-linear
    - The middle 60 percent is where springs are very linear
    - 
"""
import math
import units as u

class Material(object):
    STEEL = 'steel'
    
    def __init__(self, material):
        if material.lower() == self.STEEL:
            self.youngs_modulus = 29e6 * u.psi
            self.poisson_ratio  = 0.3
            self.density        = 0.284 * u.lb / pow(u.inch, 3.0)
        else:
            print 'I am not sure about that material'
            
    def shear_modulus(self):
        return self.youngs_modulus / (2*(1+self.poisson_ratio))


class Spring(object):
    def __init__(self, mean_diameter, wire_diameter, free_length, num_coils, material):
        self.mean_diameter = float(mean_diameter)
        self.wire_diameter = float(wire_diameter)
        self.free_length   = float(free_length)
        self.num_coils     = float(num_coils)
        self.material      = material
        
    def inside_diameter(self):
        return self.mean_diameter - self.wire_diameter

    def outside_diameter(self):
        return self.mean_diameter + self.wire_diameter

    def spring_constant(self):
        num = self.material.shear_modulus() * math.pow(self.wire_diameter,4)
        den = 8*math.pow(self.mean_diameter,3)*self.num_coils
        return num / den
        
    def coil_pitch(self):
        return self.free_length / self.num_coils
        
    def rise_angle(self):
        return math.atan2(self.coil_pitch(), math.pi*self.mean_diameter)
        
    def solid_height(self):
        return self.wire_diameter*(self.num_coils+2)
        
    def max_displacement(self):
        return self.free_length - self.solid_height()
    
    def wire_length(self):
        return math.pi*self.mean_diameter*(self.num_coils / math.cos(self.rise_angle()) + 2)
        
    def max_force(self):
        return self.spring_constant() * (self.free_length - self.solid_height())
        
    def spring_index(self):
        #The ranges for this are 4-12 with optimal suggested by efunda at 9
        return self.mean_diameter / self.wire_diameter
        
    def whal(self):
        C = self.spring_index()
        return (4*C-1)/(4*C-4) + 0.615/C
    
    def max_shear(self):
        return ( 8*self.whal()*self.mean_diameter*self.max_force() /
                 (math.pi*pow(self.wire_diameter,3.0)) )
        
    def print_properties(self, units='SI', name=''):
        if name:
            print '-------------------------------------'
            print 'Spring: %s' % name
            print '-------------------------------------'

        if 'en' == units.lower():
            print 'Outer diameter       :%.3f in'   % \
                (self.outside_diameter() / u.inch)
            print 'Mean diameter        :%.3f in'   % \
                (self.mean_diameter / u.inch)
            print 'Inside diameter      :%.3f in'   % \
                (self.inside_diameter() / u.inch)
            print 'Wire diameter        :%.3f in'   % \
                (self.wire_diameter / u.inch)
            print 'Free length          :%.3f in'   % \
                (self.free_length / u.inch)
            print 'Number of coils      :%.1f '       % \
                self.num_coils
            print 'Spring constant      :%.2e lbf/in' % \
                (self.spring_constant() / u.lbf * u.inch)
            print 'Spring index [5-15]  :%.1f'        % \
                self.spring_index()
            print 'Max force possible   :%.2e lbf'    % \
                (self.max_force() / u.lbf)
            print 'Max shear stress     :%.2e ksi'    % \
                (self.max_shear() / u.ksi)
            print 'Solid height         :%.3f in'     % \
                (self.solid_height() / u.inch)
            print 'Max displacement     :%.3f in'     % \
                (self.max_displacement() / u.inch)
            print 'Coil pitch           :%.3f in per coil ' % \
                (self.coil_pitch() / u.inch)
            print 'Rise angle           :%.2f deg'    % \
                (self.rise_angle()*180.0/math.pi)
            print 'Spring wire length   :%.3f in'     % \
                (self.wire_length() / u.inch)
        elif 'si' == units.lower():
            print 'Outer diameter       :%.3f m'   % self.outside_diameter
            print 'Mean diameter        :%.3f m'   % self.mean_diameter
            print 'Inside diameter      :%.3f m'   % self.inside_diameter
            print 'Wire diameter        :%.3f m'   % self.wire_diameter
            print 'Free length          :%.3f m'   % self.free_length
            print 'Number of coils      :%.1f '    % self.num_coils
            print 'Spring constant      :%.2e N/m' % self.spring_constant()
            print 'Spring index  [5-15] :%.1f'     % self.spring_index()
            print 'Max force possible   :%.2e N'   % self.max_force()
            print 'Max shear stress     :%.2e Pa'  % (self.max_shear())
            print 'Solid height         :%.3f m'   % self.solid_height()
            print 'Max displacement     :%.3f m'   % self.max_displacement()
            print 'Coil pitch           :%.3f '    % self.coil_pitch()
            print 'Rise angle           :%.2f deg' % \
                (self.rise_angle()*180.0/math.pi)
            print 'Spring wire length   :%.3f m'   % self.wire_length()
            print 'Shear Modulus        :%0.2e Pa' % \
                (self.material.shear_modulus()/1e3)
        else:
            print 'Units should be either SI or EN'
            
    @staticmethod
    def solve_diameter(mean_diameter, num_coils, spring_constant, material):
        """ Given a spring diameter and length, solve for the wire diameter
            to yield the desired spring constant.
        """
        num = 8.0*spring_constant*num_coils*pow(mean_diameter, 3.0)
        den = material.shear_modulus()
        return pow(num / den, 0.25)

if __name__ == '__main__':
    steel  =  Material(Material.STEEL)
    efunda = Spring((0.500-0.035)*u.inch, 0.035*u.inch, 1*u.inch, 8, steel)
    efunda.print_properties('En', 'efunda')
    
    d_mean  = (0.5-0.035)*u.inch
    n_coils = 12
    k       = 2.6*u.lbf/u.inch
    d_wire = Spring.solve_diameter(d_mean, n_coils, k, steel)
    print '\nThe recommended spring diameter is: %.3f in (efunda)' % \
        (d_wire / u.inch)



