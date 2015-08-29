# tol-bot update 1
Tree of Life bot (Python 2.7) </br>
<b>update 1</b> includes the new farm function which will farm automatically in game (see farm docstring) <br>
Status: Work in progress, some automation completed, some functions/methods need improvement </br>
Libraries used: os, time, pywin32, PIL, & tesseract (or pytesser) </br>
Check docstrings in main.py for more info </br>
- class Coords holds the coordinates of key areas of the game (buttons and regions)
- class Control handles mouse/camera movement, character movement, and more
- class ImgProc manages, processes, and analyses images </br>
Todo: Develop a way for the program to recognize objects in game such as trees, ore veins, etc. </br>
Possible methods for object recognition: 
- find image manipulations to obtain a binary image makes important objects obvious (libs: matlab, scikit/scipy, PIL)
- program a neural network for it to teach itself what a certain object looks like
