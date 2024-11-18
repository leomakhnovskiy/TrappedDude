'''Window resolution: 1280x720'''

from tkinter import *
from pages import PageControl
from values import *


window = Tk()   # Creating tkinter window
window.title('Trapped Dude')   # Setting tkinter window title
window.geometry('1280x720')     # Setting tkinter window size
window.config(bg=COL2)  # set background colour

pagecontrol = PageControl(window)

window.mainloop() 
