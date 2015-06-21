import os
import time
import win32api, win32con
import Image
import numpy as np
import tesseract
from PIL import ImageOps, ImageFilter, ImageGrab


"""
Objective: Automate tasks in the game Tree of Life
Method/Hyp: 1. Build framework for basic macros and simple input (Control class)
            2. Create system that can analyze a screenshot & distinguish an object (ImageProc class)
Author(s): James T
Screen Resolution developed for: 2560 x 1440
Game in Windowed Mode, maximized
Completed Tasks: dirt digger (digDirt()), 
Todo: Research image processing libs,
      Develop image processing and object recognition
"""

# global variables, adjust this according to resolution
X_ORIG = 0
Y_ORIG = 23
WIDTH = 2560
HEIGHT = 1399

"""
Collection of coordinates of buttons & regions each adjusted for arbitary resolution based on global vars
"""
class Coords:

    # buttons
    exit_button = (WIDTH / 2, int(0.6283 * HEIGHT))
    lobby_button = (WIDTH / 2, int(0.5475 * HEIGHT))

    # screen regions
    crosshair_box = (int(WIDTH * 0.4945), int(HEIGHT * 0.4811),
                     int(WIDTH * 0.5055), int(HEIGHT * 0.5018))
    obj_title_box = (int(WIDTH * 0.3992), int(HEIGHT * 0.0121),
                    int(WIDTH * 0.6004), int(HEIGHT * 0.0729))
 
"""
The Control class handles all mouse & keyboard input using win32api & win32con (pywin32)
List of all methods:
getCoords, holdLMB, releaseLMB, holdRMB, releaseRMB, startWalk, stopWalk, moveMouse, moveCamera, resetCamera
selectOption, loot, accessInv, selectItem, returnToLobby exitGame, ...
"""
class Control:

    def __init__(self):
        pass

    def getCoords(self):
        # updates, prints, & returns self.x, self.y (current mouse coordinates)
        x,y = win32api.GetCursorPos()
        self.x = x - X_ORIG
        self.y = y - Y_ORIG
        print 'Mouse pos: ' + str(self.x) + ' ' + str(self.y)
        return self.x, self.y

    def clickLMB(self):
        self.holdLMB()
        self.releaseLMB()

    def clickRMB(self):
        self.holdRMB()
        self.releaseRMB()

    def holdLMB(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
        time.sleep(.1)
        print 'LMB is held down...'

    def releaseLMB(self):
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        print 'LMB released'

    def holdRMB(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
        time.sleep(.1)
        print 'RMB is held down...'

    def releaseRMB(self):
        time.sleep(.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)
        print 'RMB released'

    def startWalk(self):
        win32api.keybd_event(0x57,0,0,0)
        print 'w is held down...'

    def stopWalk(self):
        win32api.keybd_event(0x57,0,win32con.KEYEVENTF_KEYUP,0)
        print 'w is released'

    def moveMouse(self, coords):
        # coords should be a tuple
        win32api.SetCursorPos(coords)
        print 'Mouse moved to: ' + str(coords) 

    def moveCamera(self, direction, offset = 450):
        self.getCoords()
        if direction == 'up':
            coords = (self.x, self.y - offset)
        elif direction == 'right':
            coords = (self.x + offset, self.y)
        elif direction == 'down':
            coords = (self.x, self.y + offset)
        elif direction == 'left':
            coords = (self.x - offset, self.y)
        self.moveMouse(coords)
        print 'Moving camera ' + direction

    def resetCamera(self):
        # resets camera horizontally - may need tweaking
        time.sleep(.1)
        for loop in range(7):
            time.sleep(.1)
            self.moveCamera('up', HEIGHT / 7)
        time.sleep(.15)
        for loop in range(2):
            time.sleep(.1)
            self.moveCamera('down', int(HEIGHT / 4))
        time.sleep(.1)
        self.moveCamera('down', int(HEIGHT / 8))
        print 'Camera reset horizontally'

    # selects one of the options by holding RMB, moving mouse, & releasing RMB
    def selectOption(self,direction):
        self.holdRMB()
        self.getCoords() # updates to current mouse coords
        offset = 300 # offset for numb of pixels mouse moves, adj for diff res
        if direction == 'up':
            coords = (self.x, self.y - offset)
        elif direction == 'right':
            coords = (self.x + offset, self.y)
        elif direction == 'down':
            coords = (self.x, self.y + offset)
        elif direction == 'left':
            coords = (self.x - offset, self.y)
        time.sleep(.2)
        self.moveMouse(coords)
        time.sleep(.2)
        self.releaseRMB()
        print direction + ' option selected'

    def loot(self):
        # hexCode Virutal key code, 0x46 = f
        win32api.keybd_event(0x46,0,0,0)
        win32api.keybd_event(0x46,0,win32con.KEYEVENTF_KEYUP,0)
        print 'Input: f'

    def isInvOpen(self):
        # Todo: check by extracting piece of screenshot & read text or RGB values
        pass

    def accessInv(self):
        win32api.keybd_event(0x45,0,0,0)
        win32api.keybd_event(0x45,0,KEYEVENTF_KEYUP,0)
        print 'Input: e'

    # This selects an item in the hotbar (1-8)
    def selectItem(self,key):
        hb_ref = {1:0x31, 2:0x32, 3:0x33, 4:0x34, 5:0x35, 6:0x36, 7:0x37, 8:0x38}
        win32api.keybd_event(hb_ref[key],0,0,0)
        win32api.keybd_event(0x45,0,KEYEVENTF_KEYUP,0)
        print 'Input: ' + str(key)

    def returnToLobby(self):
        win32api.keybd_event(0x1B,0,0,0)
        win32api.keybd_event(0x1B,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(1)
        self.moveMouse(Coords.return_lobby_button)
        self.clickLMB()
        
    def exitGame(self):
        # Todo: exit game by clicking since sending alt+f4 didn't work inside the game
        # 0x12 = alt (hex Virtual key code), 0xb8 = alt (bScanCode)
        # 0x74 = f4
        win32api.keybd_event(0x1B,0,0,0)
        win32api.keybd_event(0x1B,0,win32con.KEYEVENTF_KEYUP,0)
        self.moveMouse(Coords.exit_button)
        self.clickLMB()
        print 'Input: esc'
        
"""
Processes, modifies, and analyses images
"""
class ImgProc:

    def __init__(self, dir_plus_name = None):
        self.root_dir = os.getcwd()
        self.cropped_imgs_dir = self.root_dir + '\\cropped_imgs\\'
        self.ss_dir = self.root_dir + '\\ss\\'
        self.out_dir = self.root_dir + '\\output_imgs\\'

        if not dir_plus_name:
            self.screenGrab()
        else:
            self.file_name = dir_plus_name.split('\\')[-1]
            self.dir_plus_name = dir_plus_name
            
        self.openImg(self.dir_plus_name)
        
    def openImg(self, dir_plus_name):
        self.img = Image.open(dir_plus_name)
        self.size = self.img.size
        self.img.load() # required to split
        
        # if RGBA, converts to RGB - might be replaceable with self.img = self.img.convert('RGB')
        if len(self.img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = self.img.split()
            self.img = Image.merge("RGB", (r, g, b))

    def cropImg(self, box):
        # this crops the image to box dimensions, saves to /cropped_imgs/ folder, & re opens with new cropped image
        img_crop = self.img.crop(box)
        new_name = 'cropped_img' + str(time.time()) + '.jpg'
        self.dir_plus_name = self.cropped_imgs_dir + new_name
        self.saveImg(img_crop, self.dir_plus_name)
        self.openImg(self.dir_plus_name)

    def saveImg(self, image, dir_plus_img):
        # 1. image is the object for the save method, 2. dir_and_img is the full path + image name
        image.save(dir_plus_img)

    def updateSize(self):
        self.size = self.img.size
        print self.size

    def screenGrab(self):
        the_time = time.strftime("%d-%b-%Y;%I.%M.%S", time.localtime())
        self.file_name = 'tol_' + the_time + '.jpg'
        self.dir_plus_name = self.ss_dir + self.file_name
        box = (X_ORIG, Y_ORIG, WIDTH, HEIGHT)
        ss = ImageGrab.grab(box)
        self.saveImg(ss, self.dir_plus_name)

    def readPixels(self):
        # prints the RGB values of all the pixels in given picture - use with caution, slow w/ big img
        averages = [0,0,0]
        row_averages = [0,0,0]
        self.updateSize()

        # finds & prints the average RGB values of each row of pixels & all the pixels
        for y in xrange(self.size[1]):
            for i in range(3):
                row_averages[i] = row_averages[i] / self.size[0]
                averages[i] += row_averages[i] # adds up the row averages to find the total average
            print 'Row averages: ' + str(row_averages)
            print
            row_averages = [0,0,0] # reset for next row
            for x in xrange(self.size[0]):
                 rgb_tuple = self.img.getpixel((x,y))
                 for i in range(3):
                     row_averages[i] += rgb_tuple[i]
            
        for i in range(3):
            averages[i] = averages[i] / self.size[1]
        print 'Avg RGB values: ' + str(averages)

        self.averages = averages

    def modImg(self, method):
        if method == 1:
            # Helps identify trees easier; changes img to grayscale, soalrizes, and smooths 
            self.img = ImageOps.grayscale(self.img)
            self.img = ImageOps.solarize(self.img, 85)
            self.img = self.img.filter(ImageFilter.SMOOTH_MORE)

        elif method == 2:
            # Todo: using a different library such as scipy for img processing
            pass
        
        self.dir_plus_img = self.out_dir + self.file_name
        self.saveImg(self.img, self.dir_plus_img)
        self.openImg(self.dir_plus_name)

    def isTree(self):
        avg = self.averages
        for i in range(3):
            if avg[i] > 106:
                return True
        return False

    def checkObjTitle(self, a_str):
        # gets object title & compares the text
        self.cropImg(Coords.obj_title_box)
##        img_str = image_to_string(self.img) # pytesser
        api = tesseract.TessBaseAPI()
        api.SetOutputName("outputName");
        api.Init(".","eng",tesseract.OEM_DEFAULT)
        api.SetPageSegMode(tesseract.PSM_AUTO)
        mImgFile = self.file_name
        pixImage=tesseract.pixRead(mImgFile)
        api.SetImage(pixImage)
        outText=api.GetUTF8Text()
        print("OCR output:\n%s"%outText);
        api.End()
        if a_str.lower() in outText.lower():
            return True
        return False

    def updateImg(self):
        # takes a new screenshot and opens it up
        self.screenGrab()
        self.openImg(self.dir_plus_name)
        
# global objects
ctrl = Control()
img_obj = ImgProc()

# delete this func later
def readPixels(img_name):
    img = Image.open(img_name)
    rgb_img = img.convert('RGB')
    size = img.size
    r, g, b = rgb_img.getpixel((1, 1))
    print size
    print r, g, b
    for y in range(0, size[1]):
        print
        for x in range(0, size[0]):
             print rgb_img.getpixel((x,y))

# my 1st collection of methods that does something useful in game
def digDirt(loops):
    for x in range(loops):
        time.sleep(1.5)
        ctrl.selectOption('left')
        ctrl.loot()
        time.sleep(1.5)
        ctrl.loot()
        print 'Loop index: ' + str(x)

def treeBuddy():
    camera_move_offset_horiz = WIDTH / 70
    camera_move_offset_vert = HEIGHT / 70
    tree_found = False
    ctrl.resetCamera()
    for i in range(15):
        ctrl.moveCamera('left',camera_move_offset_horiz)
        img_obj.updateImg()
        img_obj.cropImg(Coords.crosshair_box)
        img_obj.modImg(1)
        img_obj.readPixels()
        if img_obj.isTree():
            print 'Tree...maybe'
            tree_found = False
            for i in range(2):
                ctrl.moveCamera('up',camera_move_offset_horiz)
                img_obj.updateImg()
                img_obj.cropImg(Coords.crosshair_box)
                img_obj.modImg(1)
                img_obj.readPixels()
                if not img_obj.isTree():
                    tree_found = False
                    break
                tree_found = True
            ctrl.resetCamera()
            if tree_found:
                approachTree_getWood()

def approachTree_getWood():
    # walks foward continuously checking for tree (object title)
    # if tree in range, cuts it then finds and cuts log
    atk_time = 8 # seconds required to chop tree
    log_cut = False
    camera_move_offset_horiz2 = WIDTH / 10
    while True:
        ctrl.startWalk()
        time.sleep(.1)
        ctrl.stopWalk()
        if img_obj.checkObjTitle('Tree'):
            ctrl.stopWalk()
            ctrl.holdLMB()
            time.sleep(atk_time) 
            ctrl.releaseLMB()
            print 'TREE CUT'
            for i in range(10):
                if img_obj.checkObjTitle('Log'):
                    ctrl.holdLMB()
                    time.sleep(atk_time * 0.4) # seconds required to chop log 
                    ctrl.releaseLMB()
                    print 'LOG CUT'
                    log_cut = True
                    break
                else:
                    ctrl.moveCamera('left', camera_move_offset_horiz2)
            break

def main():
    root_dir = os.getcwd()
    time.sleep(2)
##    treeBuddy()    
    img_obj.checkObjTitle('main')
    
if __name__ == '__main__':
    main()
