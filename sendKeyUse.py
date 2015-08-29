import ImageGrab
import os
import time
import win32api, win32con
import SendKeys

"""
Screen Resolution: 2560 x 1440
Game in Windowed Mode, maximized
"""

x_orig = 0
y_orig = 23

def screenGrab():
    box = (x_orig, y_orig, 2559 - x_orig, 1399 - y_orig)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap_' + str(int(time.time())) +
'.png', 'PNG')

        
def main():
    loop = [0,0,0,0,0]
    for var in loop:
        ctrl = Control()
        ctrl.wait(3.5)
        ctrl.selectLeftOption()
        ctrl.loot()
        
 
if __name__ == '__main__':
    main()
