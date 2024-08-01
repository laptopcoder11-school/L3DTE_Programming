# -------------------------------------------
# Wack a Mole GUI Game using pyqt5
# Made for L3DTE Programming Asssessment
# -------------------------------------------

# Imports
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 

#Declare constants
WINDOW_WIDTH = 700
WINDOW_HIGHT = 800
WINDOW_X = 600
WINDOW_Y = 100

#create window class 
class Window(QMainWindow):

    #This method initialises the window class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wack A Mole")
        self.setGeometry(WINDOW_X,WINDOW_Y,WINDOW_WIDTH,WINDOW_HIGHT)
        self.show()

#Main Program
if __name__ == "__main__":
    #Create the QApplication
    app = QApplication(sys.argv)
    #Create the window object
    window = Window()
    #run the application
    sys.exit(app.exec_())

