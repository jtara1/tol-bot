# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 15:59:37 2015

@author: James
"""
import PIL
from pytesser import image_to_string

print int('50\n\n')

print range(1)

img = PIL.Image.open('numb_in_pic.png')

print (image_to_string(img))