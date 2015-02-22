# -*- coding: utf-8 -*-
"""
Created on Sat Feb  7 12:43:10 2015

@author: Christopher R. Carlson, crcarlson@gmail.com

Incomplte set of conversion constants to and from Si units

Usage:
import units as u

x     = 2 * u.ft            # x is in SI meters, '2' is in feet
y_in  = 3 / u.ft            # y is in feet, '3' is in SI meters
"""

inch   = 0.0254                # inches to meters
ft     = 12*inch               # ft to meters
ksi    = 6.89475908677537e6    # ksi to pa
psi    = 6894.75729            # psi to pa
lb     = 0.453592              # lbf to kg
oz     = lb/16.0               # oz to kg
lbf    = 4.44822               # lbf to N
ozf    = lbf/16.0              # ozf to N
grains = 6.479891e-5           # grains to kg
g      = 9.81                  # m/s^2 


