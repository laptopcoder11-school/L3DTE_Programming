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

GAMEBOARD_SIZE = 5
GRIDBUTTON_SIZE = 70

#Create the WackAMole Game class, inherit from QWidget to allow window display
class WackAMole(QWidget):

    #This function initialises the window class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wack A Mole")
        self.setGeometry(WINDOW_X,WINDOW_Y,WINDOW_WIDTH,WINDOW_HIGHT)
        self.init_ui()

    #This function initalises the UI
    def init_ui(self):
        self.display_button_grid()
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setFont(QFont('Arial', 12))
        self.show()

    #This function displays the grid of buttons
    def display_button_grid(self):
        #create the layout object and grid list of buttons
        self.layout = QGridLayout()
        self.button_grid = [QPushButton(f"{n}") for n in range(GAMEBOARD_SIZE*GAMEBOARD_SIZE)]
        #set the button size
        [b.setFixedSize(GRIDBUTTON_SIZE,GRIDBUTTON_SIZE) for b in self.button_grid]
        #add the buttons to the grid layout
        [self.layout.addWidget(self.button_grid[(x*GAMEBOARD_SIZE)+y],x,y) for x in range(GAMEBOARD_SIZE) for y in range(GAMEBOARD_SIZE)]
        #attach a function to the buttons
        [b.clicked.connect(self.grid_button_clicked) for b in self.button_grid]

        #set the layout
        self.setLayout(self.layout)

    #This function runs when a button on the grid is clicked
    def grid_button_clicked(self):
        button = self.sender()
        #print the index of the button to the console
        print(self.button_grid.index(button))


#Main Program
if __name__ == "__main__":
    #Create the QApplication
    app = QApplication(sys.argv)
    #Create the game object
    game = WackAMole()
    #run the application
    sys.exit(app.exec_())