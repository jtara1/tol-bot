import os
import time
import win32api, win32con
import numpy as np
import pytesser
from PIL import ImageOps, ImageFilter, ImageGrab, Image
from string_to_int import letter_to_snumb

"""
Objective: Automate tasks in the game Tree of Life
Method/Hyp: 1. Build framework for basic macros and simple input (Control class)
            2. Create system that can analyze a screenshot & distinguish an object (ImageProc class)
Author(s): James Taracevicz
Screen Resolution developed for: 2560 x 1440
Game in Windowed Mode, maximized
Completed Tasks: dirt digger (digDirt()), 
Todo: Research image processing libs,
      Use image processing and implement object recognition
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
    exit_button = (int(WIDTH / 2), int(0.6283 * HEIGHT))
    lobby_button = (int(WIDTH / 2), int(0.5475 * HEIGHT))
    start_button = (int(WIDTH / 2), int(0.9543 * HEIGHT)) # fix later

    # screen regions
    crosshair_box = (int(WIDTH * 0.4945), int(HEIGHT * 0.4811),
                     int(WIDTH * 0.5055), int(HEIGHT * 0.5018))
    obj_title_box = (int(WIDTH * 0.3992), int(HEIGHT * 0.0121),
                    int(WIDTH * 0.6004), int(HEIGHT * 0.0729))
    current_hunger_box = (int(WIDTH * 0.1542), int(HEIGHT * 0.9292),
                          int(WIDTH * 0.1797), int(HEIGHT * 0.9543))

 
"""
The Control class handles all mouse & keyboard input using win32api & win32con (pywin32)
List of all methods:
getCoords, holdLMB, releaseLMB, holdRMB, releaseRMB, startWalk, stopWalk, moveMouse, moveCamera, resetCamera
selectOption, loot, accessInv, selectItem, returnToLobby exitGame, ...
"""
class Control:

    def __init__(self):
        self.key_ref = {'up':0x57,'right':0x44,'down':0x53,'left':0x41}
        self.hb_ref = {1:0x31, 2:0x32, 3:0x33, 4:0x34, 5:0x35, 6:0x36, 7:0x37, 8:0x38}

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

    def startWalk(self, direction):
        win32api.keybd_event(self.key_ref[direction],0,0,0)
        print 'Char started moving ' + direction

    def stopWalk(self, direction):
        win32api.keybd_event(self.key_ref[direction],0,win32con.KEYEVENTF_KEYUP,0)
        print 'Char stopped moving ' + direction
        
    def walk(self, direction, time2, jump=False):
        self.startWalk(direction)
        if jump:
            self.jump()
        time.sleep(time2)
        self.stopWalk(direction)

    def moveMouse(self, coords):
        # coords should be a tuple
        win32api.SetCursorPos(coords)
        print 'Mouse moved to: ' + str(coords) 

    def moveCamera(self, direction, offset = 450):
        self.getCoords()
        if direction == 'up':
            coords = (self.x, self.y - offset + Y_ORIG)
        elif direction == 'right':
            coords = (self.x + offset, self.y + Y_ORIG)
        elif direction == 'down':
            coords = (self.x, self.y + offset + Y_ORIG)
        elif direction == 'left':
            coords = (self.x - offset, self.y + Y_ORIG)
        self.moveMouse(coords)
        print 'Moving camera ' + direction

    def resetCamera(self, pos='neutral'):
        # resets camera horizontally - needs tweaking & testing
        if pos == 'neutral':
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
            
        elif pos == 'down':
            for i in range(12):
                time.sleep(.1)
                self.moveCamera('down', HEIGHT / 10)
                 

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
        
    def jump(self):
        win32api.keybd_event(0x20,0,0,0)
        win32api.keybd_event(0x20,0,win32con.KEYEVENTF_KEYUP,0)
        print 'Input: Spacebar'

    def accessInv(self):
        win32api.keybd_event(0x45,0,0,0)
        win32api.keybd_event(0x45,0,win32con.KEYEVENTF_KEYUP,0)
        print 'Input: e'


    def selectItem(self,key):
        # This selects an item in the hotbar (1-8)
        win32api.keybd_event(self.hb_ref[key],0,0,0)
        win32api.keybd_event(self.hb_ref[key],0,win32con.KEYEVENTF_KEYUP,0)
        print 'Input: ' + str(key)
        
    def eatFood(self,key):
        #
        self.selectItem(key)
        time.sleep(1)
        self.selectOption('left')
        self.selectItem(1)
        
    def enterGame(self):
        # enters game from character select / lobby
        self.moveMouse(Coords.start_button)
        time.sleep(.5)
        self.clickLMB()
        time.sleep(35) # seconds required to load game        
        
    def returnToLobby(self):
        win32api.keybd_event(0x1B,0,0,0)
        win32api.keybd_event(0x1B,0,win32con.KEYEVENTF_KEYUP,0)
        time.sleep(1)
        self.moveMouse(Coords.lobby_button)
        self.clickLMB()
        time.sleep(15) # seconds required to load to lobby
        print 'Logged out to lobby'
        
    def exitGame(self):
        # 0x12 = alt (hex Virtual key code), 0xb8 = alt (bScanCode)
        # 0x74 = f4
        win32api.keybd_event(0x1B,0,0,0)
        win32api.keybd_event(0x1B,0,win32con.KEYEVENTF_KEYUP,0)
        self.moveMouse(Coords.exit_button)
        self.clickLMB()
        print 'Game exited'
        
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
        
    def clusterPixels(self):
        # incomplete, experimental - clusters pixels
        W = self.size[0]
        H = self.size[1]
        WK = 4 # cluster size
        HK = 4
        # finds a proper cluster size to evenly fit entire img            
        while True:            
            if W % WK == 0:
                break
            WK += 1
        while True:
            if H % HK == 0:
                break
            HK += 1

        index = 0
        area = ((W / WK) * (H / HK))
        clusters = np.empty(area) 

        #debug
        print 'size: ' + str(self.img.size)
        print 'WK: ' + str(WK)
        print 'HK: ' + str(HK)
        
        for h in range(0,H,HK):
            for w in range(0,W,WK):
                cluster = []
                
                for hk in range(HK):
                    
                    for wk in range(WK):
                        pixel = np.empty(3)
                        pix_val = self.img.getpixel((w+wk,h+hk))                        
                        pixel[0], pixel[1], pixel[2] = pix_val[0], pix_val[1], pix_val[2]                        
#                        cluster.append(pix_val)
                clusters[index] = cluster                        
                index += 1
        
        print clusters
                    
                    
    def isTree(self):
        avg = self.averages
        for i in range(3):
            if avg[i] < 106:
                return True
        return False

    # test this method
    def checkObjTitle(self, a_str):
        # gets object title & compares the text
        self.updateImg()
        self.cropImg(Coords.obj_title_box)
        img_str = pytesser.image_to_string(self.img)
        if a_str.lower() in img_str.lower():
            return True
        return False
        
    def isHungry(self):
        # needs testing
        self.updateImg()
        self.cropImg(Coords.current_hunger_box)
        img_str = pytesser.image_to_string(self.img)
        img_str = letter_to_snumb(img_str) # uses the func I made to convert letter o to number 0 in a string
        print img_str # debug
        hunger = int(img_str) # uses the func get_int from string_to_int.py that I created
        if hunger <= 300:
            return True
        return False

    def updateImg(self):
        # takes a new screenshot and opens it up
        self.screenGrab()
        self.openImg(self.dir_plus_name)
        

def treeBuddy():
    """
    Does not work at the moment
    Still need to create object recognition
    """
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
                ctrl.moveCamera('up',camera_move_offset_vert)
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
    """
    Does not work at the moment
    walks foward continuously checking for tree (object title)
    if tree in range, cuts it then finds and cuts log
    """ 
    atk_time = 8 # seconds required to chop tree
    log_cut = False
    camera_move_offset_horiz2 = WIDTH / 10
    while True:
        ctrl.startWalk()
        time.sleep(.25)
        ctrl.stopWalk()
        img_obj.updateImg()
        if img_obj.checkObjTitle('tree'):
            ctrl.stopWalk()
            ctrl.holdLMB()
            time.sleep(atk_time) 
            ctrl.releaseLMB()
            print 'TREE CUT'
            for i in range(10):
                img_obj.updateImg()
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
   
def farm(w,h,status='harvest',loops=1):
    """     
    2nd collection of Control methods that automates Tree of Life gameplay
    STATUS: 7/2/2015 This mostly works - adjust time variables. When relogging, character is sometimes misplaced (randomly?)
    PURPOSE: harvests (seeds & plants) & replants a rectangular-sized farm
    INSTRUCTIONS: begin with character on bottom right, char standing on farm patch, seeds selected on hotbar 1
    PARAMETERS: w = width of farm, h = height of farm, status ('harvest' or 'new'), new will plant seeds on empty field, loops = number of times entire function will loop
    """
    h1 = int(h/2) # var to get seeds from first half (or fewer) of rows
    food_key = 5 # hotbar key for food
    dirt_place_time = 4.5
    walk_time = 0.33
    wait_time = 0.7
    grow_time = 540 # time for plants to grow = 600s - (time to log out & in) 
    
    ctrl.resetCamera('down')
    for loop in range(loops):
        for y in range(h):
            for x in range(w):
                # checks if char is hungry before moving, & eats food on food_key
                if img_obj.isHungry():
                    ctrl.eatFood(key=food_key)
                if status == 'harvest':
                    # picks up farm patch, loot seeds, places farm patch, continues            
                    if y < h1:  
                        ctrl.selectOption('down')
                        time.sleep(dirt_place_time) # takes 3 sec + more time due to server lag
                        ctrl.selectOption('right')
                        ctrl.loot()                
                        
                        ctrl.walk('down', walk_time * 2, jump=True)
                        ctrl.selectOption('down')
                        ctrl.clickLMB()
                        time.sleep(dirt_place_time)
                        
                        ctrl.walk('up', walk_time, jump=True)
    
                    else:
                        ctrl.selectOption('right')
                        for i in range(12): # takes 5 seconds to harvest, in 6 seconds, f key is pressed 12 times
                            ctrl.loot()
                            time.sleep(.5)
                            
                time.sleep(wait_time) # delay to make sure it jumps to the next patch
                # plants seeds - assumes char is holding seeds
                ctrl.selectOption('right')
                for i in range(12): # takes 5 seconds to harvest, in 5.5 seconds, f key is pressed 11 times
                    ctrl.loot()
                    time.sleep(.5)
                time.sleep(wait_time)
                
                # moves char to next farm patch
                if x != (w-1): # if not on last farm patch of row
                    if y % 2 == 0:
                        direction = 'left'
                    else:
                        direction = 'right'
                    ctrl.walk(direction, walk_time, jump=True)
                time.sleep(wait_time) # delay for server lag
            
            # moves char up to next row if not on last row
            if y != (h-1):
                ctrl.walk('up', walk_time, jump=True)
    
        # final loot loop to get remaining items
    #    for i in range(10):
    #        ctrl.loot()
    #        time.sleep(.5)
        
        # returns char to bottom right farm patch
        if (h) % 2 != 0: # if height is odd, move char to right side
            for x in range(w-1):
                ctrl.walk('right', walk_time, jump=True)
                time.sleep(wait_time)
        for y in range(h-1):
            ctrl.walk('down', walk_time * 2, jump=True)
            time.sleep(wait_time)
    
        # returns to lobby, waits for plants to grow, logs in
        ctrl.returnToLobby()
        time.sleep(grow_time)
        ctrl.enterGame()
        # resets camera to be aligned facing North as camera will always be pointed North after logging in
        ctrl.walk('up', .1, jump=True) 
        time.sleep(wait_time)
        ctrl.walk('down', .1, jump=True)
        
        ctrl.resetCamera('down')
        # when relogging, char is displaced sometimes, this checks if field is selected, if not it'll try to find it, if that fails the program exits
        if not (img_obj.checkObjTitle('field')):
            ctrl.walk('left', walk_time, jump=True)
            if not (img_obj.checkObjTitle('field')):
                ctrl.walk('up', walk_time, jump=True)
                if not (img_obj.checkObjTitle('field')):
                    break
   
   
def digDirt(loops):
# my 1st collection of methods that does something useful in game
    for x in range(loops):
        time.sleep(1.5)
        ctrl.selectOption('left')
        ctrl.loot()
        time.sleep(1.5)
        print 'Loop index: ' + str(x)
    time.sleep(1.5)
    ctrl.loot()

# global objects
ctrl = Control()
img_obj = ImgProc()

def main():
#    root_dir = os.getcwd()
#    other_imgs = root_dir + '\\other_imgs\\'
#    file_name = 'h-test (7).jpg'
    time.sleep(2)
#    digDirt(225)
    farm(3,2,status='harvest',loops=1)
#    farm(5,2,status='new')
#    img_obj = ImgProc('cropped_img1.jpg')
    
#    img_obj.clusterPixels()
    
if __name__ == '__main__':
    main()
