# tol-bot
Tree of Life bot </br>
Status: Work in progress, some automation completed </br>
Check docstrings in main.py for more info
1. Class info:
- class Coords holds the coordinates of key areas of the game (buttons and regions)
- class Control handles mouse/camera movement, character movement, and more
- class ImgProc manages, processes, and analyses images 
2. Todo: Develop a way for the program to recognize objects in game such as trees, ore veins, etc. 
3. Possible methods for object recognition: 
- apply enough image manipulation until a binary-color image makes important objects obvious (libs: matlab, scikit/scipy, PIL)
- program a neural network for it to teach itself what a certain object looks like
