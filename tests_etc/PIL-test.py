# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 14:49:04 2015

@author: James
"""

#import PIL
from PIL import ImageOps, ImageFilter, ImageGrab, Image
import os


fp = os.getcwd() + '\\trees_ss 8.jpg\\'
img = Image.open('trees_ss 8.jpg', 'r')    
#labels = img.split
#print labels
pixel = img.getpixel((1,1))
r, g, b = img.split()
print r