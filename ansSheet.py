#Answer screen
import sys
import os
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWidgets import QMessageBox
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets, QtGui, QtCore

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from clientGen import *
import time

from pyside_material import apply_stylesheet

import sharedSpace




class AnsSheet(QtWidgets.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        #QtWidgets.QWidget.__init__(self)
        super(AnsSheet, self).__init__()

        self.timerVal=0 #the game timer
        self.timerFlag=0
        

        self.selectionV=[0,0] #this is a main array
        
        self.setWindowTitle('Answer Sheet')
        
        self.load_ui()
        self.center()    

        # self.lb1 = self.findChild(QtWidgets.QLabel, "lb1")
        # self.lbMain = self.findChild(QtWidgets.QLabel, "lbMain")
        self.b1= self.findChild(QtWidgets.QPushButton,'b1')
        self.b2= self.findChild(QtWidgets.QPushButton,'b2')
        self.b3= self.findChild(QtWidgets.QPushButton,'b3')
        # self.lb1.setText(str(self.timerVal))

        self.lbl1= self.findChild(QtWidgets.QLabel,'lbl1')
        self.lbl2= self.findChild(QtWidgets.QLabel,'lbl2')
        self.lbl3= self.findChild(QtWidgets.QLabel,'lbl3')
        self.lbl4= self.findChild(QtWidgets.QLabel,'lbl4')

        self.b1.clicked.connect(self.clkB1)
        self.b2.clicked.connect(self.clkB2)
        self.b3.clicked.connect(self.clkB3)

        self.lbl1.setText(sharedSpace.ingredientsText[0]+' "Ingredient#1" / 100ml')
        self.lbl2.setText(sharedSpace.ingredientsText[1]+' "Ingredient#2" / 100ml')
        self.lbl3.setText(sharedSpace.ingredientsText[2]+' "Ingredient#3" / 100ml')
        self.lbl4.setText(sharedSpace.ingredientsText[3]+' "Ingredient#4" / 100ml')

        
        self.TimerClock = QTimer()
        self.TimerClock.setInterval(1000)#Refresh the game timer after every 1 second=1 milliseconds
        self.TimerClock.timeout.connect(self.ClockTimer)
        self.TimerClock.start()

    def getfile(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file',  'c:\\',"Image files (*.jpg *.png)")

    def clkB1(self):
        print('B1')
        self.hide()

    def clkB2(self):
        print('B2')
        self.hide()

    def clkB3(self):
        print('B3')
        self.getfile()


    def loadFile(self):
        #this function loads the answer files present in the data folder
        path = os.path.join(os.path.dirname(__file__), "data",sharedSpace.filesList[sharedSpace.catVals[0]-1][sharedSpace.catVals[1]-1]+'.txt')
        g=open(path,'r')
        mv=g.read()
        g.close()
        return mv
    
    def ClockTimer(self):
        #changes the timer value after every 1 seconds
        print('ct')
       
    def center(self):
        #tires to keep the window at the center of the screen
            
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
       
        self.mqttReady=1


    def load_ui(self):
        #laods the answer screen and applies the theme
        path = os.path.join(os.path.dirname(__file__), "ansSheet.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.win=loader.load(ui_file, self)
        #win.show()
        ui_file.close()

