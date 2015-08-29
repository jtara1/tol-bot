import ImageGrab
import os
from time import strftime, localtime, time

"""
Screen Resolution: 2560 x 1440
Game in Windowed Mode, maximized
"""

x_orig = 0
y_orig = 23
def screenGrab():
    the_time = strftime("%d-%b-%Y;%I.%M.%S", localtime())
    box = (x_orig, y_orig, 2560 - x_orig, 1399)
    img = ImageGrab.grab(box)
    img.save(os.getcwd() + '\\tol_' + the_time + '.jpg', 'JPEG')
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()
