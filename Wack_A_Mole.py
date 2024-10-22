# -------------------------------------------
# Wack a Mole GUI Game using pyqt5
# Made for L3DTE Programming Asssessment
# -------------------------------------------

# Imports
import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QLabel, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import QTimer 
from PyQt5.QtGui import QFont
from random import randint
from os import path, chdir

#update the working directory to the location of the .py file to ensure images always load
chdir(path.dirname(__file__))

#Declare constants
FILE_PATH = "./assets/"
WINDOW_WIDTH = 700
WINDOW_HIGHT = 800
WINDOW_X = 600
WINDOW_Y = 100

GAMEBOARD_SIZE = 5
GRIDBUTTON_SIZE = 70

MIN_DURATION = 15
MAX_DURATION = 60

MIN_GRID_SIZE = 5
MAX_GRID_SIZE = 20

MOLE_COUNT = 6

global score

#Create the WackAMole Game class, inherit from QWidget to allow window display
class WackAMole(QWidget):

    #This function initialises the window class
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wack A Mole")
        self.setGeometry(WINDOW_X,WINDOW_Y,WINDOW_WIDTH,WINDOW_HIGHT)
        self.init_ui()

        #the state of the game, 1 = playing, 0 = ended
        self.game_state = 1
        
        #start a the tick timer
        self.timer_display = game_duration
        timer = QTimer(self)
        timer.timeout.connect(self.on_tick)
        timer.start(1000) #1000 ms = 1 s

    #This function initalises the UI
    def init_ui(self):
        self.display_button_grid()
        self.score_label = QLabel(f"Score: {score}", self)
        self.score_label.setFont(QFont('Arial', 12))
        self.timer_label = QLabel(f"Time: {game_duration}", self)
        self.timer_label.setGeometry(0,30,150,16)
        self.timer_label.setFont(QFont('Arial', 10))
        self.show()

    #This function displays the grid of buttons
    def display_button_grid(self):
        #create the layout object and grid list of buttons
        self.layout = QGridLayout()
        self.button_grid = [QPushButton(f"{""}") for n in range(GAMEBOARD_SIZE*GAMEBOARD_SIZE)]
        #set the button size
        [b.setFixedSize(GRIDBUTTON_SIZE,GRIDBUTTON_SIZE) for b in self.button_grid]
        #add the buttons to the grid layout
        [self.layout.addWidget(self.button_grid[(x*GAMEBOARD_SIZE)+y],x,y) for x in range(GAMEBOARD_SIZE) for y in range(GAMEBOARD_SIZE)]
        #attach a function to the buttons
        [b.clicked.connect(self.grid_button_clicked) for b in self.button_grid]
        #attach an image to the buttons
        [b.setStyleSheet(f"background-image : url({FILE_PATH}hole.png);") for b in self.button_grid]
        #remove the text by setting font size to really large (0 doesnt work)
        [b.setFont(QFont('Arial', 999)) for b in self.button_grid]

        self.setLayout(self.layout)

        #setup moles randomly in the grid
        for _ in range(MOLE_COUNT):
            b = self.button_grid[randint(0,(GAMEBOARD_SIZE*GAMEBOARD_SIZE) - 1)]
            b.setText("mole")
            b.setStyleSheet(f"background-image : url({FILE_PATH}moleimage.png);")
        

    #This function runs when a button on the grid is clicked
    def grid_button_clicked(self):
        if self.game_state == 1:
            global score
            button = self.sender()
            #print the index of the button to the console for debugging 
            #print(self.button_grid.index(button))
            #check if the button is a mole, and react accordingly
            if button.text() == "mole":
                score += 1
                self.score_label.setText(f"Score: {score}")
                self.move_mole_to_new_location(button)
                
    #This function moves the mole to a new randomlocation on the grid
    def move_mole_to_new_location(self, mole):
                new_location = self.button_grid.index(mole)
                #select a random cell that is not a mole
                while self.button_grid[new_location].text() == "mole":
                    new_location = randint(0,(GAMEBOARD_SIZE*GAMEBOARD_SIZE) - 1)
                #move the mole to the new location
                self.button_grid[new_location].setText("mole")
                mole.setText("")
                #update the button images
                self.button_grid[new_location].setStyleSheet(f"background-image : url({FILE_PATH}moleimage.png);")
                mole.setStyleSheet(f"background-image : url({FILE_PATH}hole.png);")

    #This function runs on every game tick mesured by the timer object
    def on_tick(self):
        if self.game_state == 1:
            #decrement and update the timer display
            self.timer_display -= 1
            self.timer_label.setText(f"Time: {self.timer_display}")
            #move the moles automatically
            [self.move_mole_to_new_location(m) for m in self.button_grid]
            #stop the game if timer is 0
            if self.timer_display == 0:
                global score
                timer.stop()
                QMessageBox.question(self, 'Wack a Mole', f"Times Up! \n Final Score : {score}" , QMessageBox.Ok, QMessageBox.Ok)
                self.game_state = 0
                self.save_score_to_file()

    #This function saves the users current score to a file (append)
    def save_score_to_file(self):
        #open a file for saving scores and append the score
        f = open("WackAMoleScores.txt", "a")
        score_infomation = f"sc:{score}, gs:{GAMEBOARD_SIZE}, tmr:{game_duration}"
        f.write(f"\n{score_infomation}")
        f.close()
        print("Saved Score")
        


#Main Program
if __name__ == "__main__":
    #Create the QApplication
    app = QApplication(sys.argv)

    #Ask the user for a game duration and grid size
    game_duration, ok = QInputDialog.getInt(QWidget(),'Input Dialog', f"Enter a game length ({MIN_DURATION} to {MAX_DURATION}):", min=MIN_DURATION, max=MAX_DURATION)
    if not ok: game_duration = MIN_DURATION #ensure value is never null 
    GAMEBOARD_SIZE, ok = QInputDialog.getInt(QWidget(),'Input Dialog', f"Enter a game grid size ({MIN_GRID_SIZE} to {MAX_GRID_SIZE}):", min=MIN_GRID_SIZE, max=MAX_GRID_SIZE)
    if not ok: GAMEBOARD_SIZE = MIN_GRID_SIZE #ensure value is never null 

    #Create a  timer and game object
    score = 0
    timer = QTimer()
    game = WackAMole()

    #run the application
    sys.exit(app.exec_())