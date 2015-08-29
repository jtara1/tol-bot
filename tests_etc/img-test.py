import os
import time
from PIL import ImageFilter, ImageEnhance, ImageOps, Image
import matplotlib.pyplot as plt
import pytesser # had to alter pytesser.py for Python(x,y) (changed import Image to from PIL import Image)
import numpy as np
import skimage

WIDTH = 2560
HEIGHT = 1399

crosshair_box = (int(WIDTH * 0.4945), int(HEIGHT * 0.4811),
                     int(WIDTH * 0.5055), int(HEIGHT * 0.5018))

in_path2 = os.getcwd() + '\\cropped_imgs\\cropped_img1434247634.12.jpg'
in_path = os.getcwd() + '\\trees.jpg'
out_path = os.getcwd() + '\\output_imgs\\out' + str(int(time.time())) + '.jpg'
img = Image.open(in_path)
##img.convert('RGB')
##crop = img.crop((1000,1000,1200,1200))

img.load() # required to split

# if RGBA, converts to RGB - might be replaceable with self.img = self.img.convert('RGB')
#if len(img.split()) == 4:
#    # prevent IOError: cannot write mode RGBA as BMP
#    r, g, b, a = img.split()
#    img = Image.merge("RGB", (r, g, b))

def find_edges(img):
    return img.filter(ImageFilter.FIND_EDGES)
def contour(img):
    return img.filter(ImageFilter.CONTOUR)
def edge_enhance1(img):
    return img.filter(ImageFilter.EDGE_ENHANCE)
def edge_enhance2(img):
    return img.filter(ImageFilter.EDGE_ENHANCE_MORE)
def blur(img):
    return img.filter(ImageFilter.BLUR)
def detail(img):
    return img.filter(ImageFilter.DETAIL)
def emboss(img):
    return img.filter(ImageFilter.EMBOSS)
def smooth1(img):
    return img.filter(ImageFilter.SMOOTH)
def smooth2(img):
    return img.filter(ImageFilter.SMOOTH_MORE)
def sharpen(img):
    return img.filter(ImageFilter.SHARPEN)

def brightness(img):
    return ImageEnhance.Brightness(img).enhance(1.95)
def contrast(img):
    return ImageEnhance.Contrast(img).enhance(.05)
def color_balance(img):
    return ImageEnhance.Color(img).enhance(0)

def readPixels(img):
    size = img.size
    for y in range(0,size[1]):
        print
        for x in range(0,size[0]):
            print img.getpixel((x,y))

def save(img):
    img.save(out_path)

def blend(img):
    bWidth = WIDTH 

##img = blur(img)
##img = detail(img)
##img = edge_enhance1(img)
##img = emboss(img)
##img = find_edges(img)
##img = contour(img)
##img = smooth1(img)
##img = smooth2(img)
##img = sharpen(img)

##img = color_balance(img)
##img = img.convert('L')
#img = brightness(img)
#img = contrast(img)
##img = img.convert('1')
#img = contour(img)

##img = ImageOps.autocontrast(img)
##img = ImageOps.equalize(img)
##img = ImageOps.grayscale(img)
##img = ImageOps.posterize(img, 1)
##img = ImageOps.solarize(img, 85)
##img = blur(img)
##img = smooth2(img)
    
##img = img.crop(crosshair_box)
##readPixels(img)



img = img.convert('L')

print img.getbands()
print img.mode
print img.size

def convert_to_binary(threshold = 170):
    # made for grayscale image ('L')
    init_clock = time.clock()
    pixel_vals = []
    size = img.size
    for y in xrange(size[1]):
        for x in xrange(size[0]):
            pixel_vals.append(img.getpixel((x,y)))
    finish_clock = time.clock()
    print finish_clock - init_clock
    
    pixel_vals = np.array(pixel_vals)
    if pixel_vals >= threshold:
        pixel_vals = 255
    else:
        pixel_vals = 0

def convert_to_binary2(threshold = 170):
    init_clock = time.clock()
    size = img.size    
    pixel_vals = np.array([0 for i in xrange(size[0]*size[1])])
    
    for y in xrange(size[1]):
        for x in xrange(size[0]):
            pixel_vals[x*y] = img.getpixel((x,y))
    finish_clock = time.clock()
    print finish_clock - init_clock

            
#convert_to_binary()
    
trees_L = skimage.data.load('trees_L.jpg')
print skimage.img_as_bool(trees_L)

#histogram = img.histogram()
#plt.plot(histogram)
#plt.show()

save(img)

print 
##save(img)
