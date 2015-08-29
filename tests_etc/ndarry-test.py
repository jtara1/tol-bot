# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:26:52 2015

@author: James
"""

import numpy as np

myarry = np.array([0 for i in xrange(14)])
myarry.fill(2)
myarry[0] = 4

print myarry