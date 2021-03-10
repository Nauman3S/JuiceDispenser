# This Python file uses the following encoding: utf-8
# This is a main program file for JPGUI project

import sys
import os

####GUI LIBRARIES
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import QFile, Signal
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets, QtGui, QtCore

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
####GUI LIBRARIES

from clientGen import * #USER ID generation file

import time #Time library

from pyside_material import apply_stylesheet #theme used in this progrram

import sharedSpace #Shared variables


from settingsScreen import * # settings main screen
from categoriesScreen import * #categories main screen

def clickable(widget):

    class Filter(QObject):
    
        clicked = Signal()
        
        def eventFilter(self, obj, event):
        
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True
            
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

class main(QMainWindow):
    #main screen
    def __init__(self):
        super(main, self).__init__()
        sharedSpace.loadSettings()
        self.settingsWindow = SettingsWindow()
        self.catWindow = CategoriesWindow()

        self.load_ui()

        self.center()
        
        self.selectedUsers=[0,0,0,0] #an array to store which user has pressed the button
        self.screenActivate=0 #active screen variable to store the active screen id
        self.screenANum=0
        
        #Buttons definition
        self.b1 = self.findChild(QtWidgets.QPushButton, "b1")
        self.b2 = self.findChild(QtWidgets.QPushButton, "b2")
        self.b3 = self.findChild(QtWidgets.QPushButton, "b3")
       
        #Arrays which stores the selected and un-selected pictures
        self.juices =[ QtGui.QPixmap(sharedSpace.drinksPath[0]),
                        QtGui.QPixmap(sharedSpace.drinksPath[1]),
                        QtGui.QPixmap(sharedSpace.drinksPath[2]),
                        QtGui.QPixmap(sharedSpace.drinksPath[3]),
                        QtGui.QPixmap(sharedSpace.drinksPath[4]),
                        QtGui.QPixmap(sharedSpace.drinksPath[5])
        ]
        

        # self.vlo2 = self.findChild(QtWidgets.QVBoxLayout, "vlo2")
        # self.vlo2.setAlignment(Qt.AlignVCenter | Qt.AlignTop)
        

        #Simple labels
        self.lb1 = self.findChild(QtWidgets.QLabel, "lb1")
        self.lb2 = self.findChild(QtWidgets.QLabel, "lb2")
        
        self.lb3 = self.findChild(QtWidgets.QLabel, "lb3")
        self.lb4 = self.findChild(QtWidgets.QLabel, "lb4")
        self.lb5 = self.findChild(QtWidgets.QLabel, "lb5")
        self.lb6 = self.findChild(QtWidgets.QLabel, "lb6")
        self.lb7 = self.findChild(QtWidgets.QLabel, "lb7")

        self.dn1 = self.findChild(QtWidgets.QLabel, "dn1")
        self.dn2 = self.findChild(QtWidgets.QLabel, "dn2")
        self.dn3 = self.findChild(QtWidgets.QLabel, "dn3")
        self.dn4 = self.findChild(QtWidgets.QLabel, "dn4")
        self.dn5 = self.findChild(QtWidgets.QLabel, "dn5")
        self.dn6 = self.findChild(QtWidgets.QLabel, "dn6")


        self.juicesLbl=[self.lb1,self.lb2,self.lb3,self.lb4,self.lb5,self.lb6]
        
        self.lb1.setPixmap(self.juices[0])
        self.lb2.setPixmap(self.juices[1])
        self.lb3.setPixmap(self.juices[2])
        self.lb4.setPixmap(self.juices[3])
        self.lb5.setPixmap(self.juices[4])
        self.lb6.setPixmap(self.juices[5])
        # for i in range(0,6):
        #     self.juicesLbl[i].setStyleSheet("QLabel::hover"
        #                                     "{"
        #                                         "background-color : rgb(232, 243, 193);"
        #                                     "}") 
        #label.show()
        self.lblExit = self.findChild(QtWidgets.QLabel, "lblExit")
        self.exitIcon=QtGui.QPixmap('img/exit.png')
        self.lblExit.setPixmap(self.exitIcon)
        clickable(self.lblExit).connect(self.exitAll)
        #self.lb1.mousePressEvent=self.doIt
        clickable(self.lb1).connect(self.juice1)
        clickable(self.lb2).connect(self.juice2)
        clickable(self.lb3).connect(self.juice3)
        clickable(self.lb4).connect(self.juice4)
        clickable(self.lb5).connect(self.juice5)
        clickable(self.lb6).connect(self.juice6)
        #lines below connect functions with the buttons
        self.b1.clicked.connect(self.clkB1)
        

        self.dn1.setText(sharedSpace.drinkNames[0])
        self.dn2.setText(sharedSpace.drinkNames[1])
        self.dn3.setText(sharedSpace.drinkNames[2])
        self.dn4.setText(sharedSpace.drinkNames[3])
        self.dn5.setText(sharedSpace.drinkNames[4])
        self.dn6.setText(sharedSpace.drinkNames[5])


        self.ActiveWinManager = QTimer()
        self.ActiveWinManager.setInterval(1000)#changed from 2000
        self.ActiveWinManager.timeout.connect(self.ActiveWin)
        self.ActiveWinManager.start()

   

    def exitAll(self):
        exit(0)
      
    def juice1(self):
        print('Juice 1')
        sharedSpace.selectedDrink="D;1"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
        

    def juice2(self):
        print('Juice 2')
        sharedSpace.selectedDrink="D;2"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
    
    def juice3(self):
        print('Juice 3')
        sharedSpace.selectedDrink="D;3"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
    
    def juice4(self):
        print('Juice 4')
        sharedSpace.selectedDrink="D;4"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
    
    def juice5(self):
        print('Juice 5')
        sharedSpace.selectedDrink="D;5"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
    
    def juice6(self):
        print('Juice 6')
        sharedSpace.selectedDrink="D;6"
        sharedSpace.activeWindow="cat"
        self.toggle_window(self.catWindow,'cat')
        self.hide()
    
    
    def center(self):
        #this function tries to keep the main window  t the center of the screen
            
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
    def checkPressedButtons(self):
        #this button keeps track of which user has pressed the button on remote
        #if all users including the moderator has pressed the buttons, the game starts
        if(all(v == 1 for v in self.selectedUsers)):
            print("start")
            self.lb5.setText("Lets Play!")
            self.screenActivate=1
            self.screenANum=1
            



    def playerPressed(self, playerNum, pressed):
        #this function change the color of the button from gray to green and vice versa
        if(playerNum==0):
            if(pressed==False):
                self.lb1.setPixmap(self.pixmapOFF[0])
            else:
                self.lb1.setPixmap(self.pixmapON[0])
        elif(playerNum==1):
            if(pressed==False):
                self.lb2.setPixmap(self.pixmapOFF[1])
            else:
                self.lb2.setPixmap(self.pixmapON[1])
        elif(playerNum==2):
            if(pressed==False):
                self.lb3.setPixmap(self.pixmapOFF[2])
            else:
                self.lb3.setPixmap(self.pixmapON[2])
        elif(playerNum==3):
            if(pressed==False):
                self.lb4.setPixmap(self.pixmapOFF[3])
            else:
                self.lb4.setPixmap(self.pixmapON[3])
        
    def buttonSelection(self, btnName, sel):
        #it applies theme to the selected button
        if(sel==True):
            btnName.setStyleSheet("QPushButton{ background-color: rgb(91,187,122); color: rgb(0, 0, 0);}")
        else:
            btnName.setStyleSheet("QPushButton{ background-color: rgb(49,54,59); color: rgb(66, 132, 242);}")

    
    
    def clkB1(self):
        print("2 clicked")
        self.toggle_window(self.settingsWindow,"settings")
        
    
   
    def ActiveWin(self):
        #toggles (open/close) the screen based on the moderator remote button press
       
        if(sharedSpace.updatePics(0)):
            print('updating')
            self.dn1.setText(sharedSpace.drinkNames[0])
            self.dn2.setText(sharedSpace.drinkNames[1])
            self.dn3.setText(sharedSpace.drinkNames[2])
            self.dn4.setText(sharedSpace.drinkNames[3])
            self.dn5.setText(sharedSpace.drinkNames[4])
            self.dn6.setText(sharedSpace.drinkNames[5])

            self.juices =[ QtGui.QPixmap(sharedSpace.drinksPath[0]),
                        QtGui.QPixmap(sharedSpace.drinksPath[1]),
                        QtGui.QPixmap(sharedSpace.drinksPath[2]),
                        QtGui.QPixmap(sharedSpace.drinksPath[3]),
                        QtGui.QPixmap(sharedSpace.drinksPath[4]),
                        QtGui.QPixmap(sharedSpace.drinksPath[5])
                        ]
            self.lb1.setPixmap(self.juices[0])
            self.lb2.setPixmap(self.juices[1])
            self.lb3.setPixmap(self.juices[2])
            self.lb4.setPixmap(self.juices[3])
            self.lb5.setPixmap(self.juices[4])
            self.lb6.setPixmap(self.juices[5])
            self.dn1.setText(sharedSpace.drinkNames[0])
            self.dn2.setText(sharedSpace.drinkNames[1])
            self.dn3.setText(sharedSpace.drinkNames[2])
            self.dn4.setText(sharedSpace.drinkNames[3])
            self.dn5.setText(sharedSpace.drinkNames[4])
            self.dn6.setText(sharedSpace.drinkNames[5])
            




        if(self.screenActivate==1):
            if(self.screenANum==1):
                self.toggle_window(self.catWindow,'cat')
            elif(self.screenANum==2):
                self.toggle_window(self.settingsWindow,"settings")
            
            self.screenActivate=0
            self.screenANum=0
            #self.client.loop()
            

    def showSettings(self, checked): #shows setting screen
        self.settingsWindow = SettingsWindow()

        apply_stylesheet(self.settingsWindow, theme='dark_blue.xml')
        
        self.settingsWindow.showFullScreen()

    def toggle_window(self, window,winName): #handle settings and categories screen open/close events
        if(winName=="settings"):
            if (window.isVisible()):
                window.hide()
            else:
                self.settingsWindow = SettingsWindow()
                
                apply_stylesheet(self.settingsWindow, theme='dark_blue.xml')
                self.settingsWindow.showFullScreen()
        elif(winName=="cat"):
            if (window.isVisible()):
                window.hide()
            else:
                self.catWindow = CategoriesWindow()

                apply_stylesheet(self.catWindow, theme='dark_blue.xml')
                self.catWindow.showFullScreen()

    def center(self):
            
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

            
    def load_ui(self):
        #load the main screen
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.win=loader.load(ui_file, self)
        #self.add_menu_theme(self.win, self.win.menuStyles)
        self.center()
        #win.show()
        ui_file.close()
    

if __name__ == "__main__":
    #load the app and apply the theme
    app = QApplication([])
    app.setStyle('Fusion')
    
    widget = main()
   # widget.setStyleSheet("background-color:black;")
    apply_stylesheet(app, theme='dark_blue.xml')
    widget.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    widget.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    #widget.setWindowFlags( Qt.FramelessWindowHint)

    #widget.win.show()
    widget.win.showFullScreen()
    sys.exit(app.exec_())
