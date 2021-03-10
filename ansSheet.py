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
import subprocess
import sharedSpace

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


class AnsSheet(QtWidgets.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        #QtWidgets.QWidget.__init__(self)
        super(AnsSheet, self).__init__()
        print('init')
        sharedSpace.loadSettings()

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
        self.keyboardIcon=QtGui.QPixmap(sharedSpace.keyboardICO)
        self.keyboard= self.findChild(QtWidgets.QLabel,'keyboard')
        self.keyboard.setPixmap(self.keyboardIcon)
        clickable(self.keyboard).connect(self.openKeyboard)

        self.lbl1= self.findChild(QtWidgets.QLabel,'lbl1')
        self.lbl2= self.findChild(QtWidgets.QLabel,'lbl2')
        self.lbl3= self.findChild(QtWidgets.QLabel,'lbl3')
        self.lbl4= self.findChild(QtWidgets.QLabel,'lbl4')

        self.ql1= self.findChild(QtWidgets.QLineEdit,'ql1')
        self.ql2= self.findChild(QtWidgets.QLineEdit,'ql2')
        self.ql3= self.findChild(QtWidgets.QLineEdit,'ql3')
        self.ql4= self.findChild(QtWidgets.QLineEdit,'ql4')
        self.ql5= self.findChild(QtWidgets.QLineEdit,'ql5')
        

        self.b1.clicked.connect(self.clkB1)
        self.b2.clicked.connect(self.clkB2)
        self.b3.clicked.connect(self.clkB3)

        self.lbl1.setText(sharedSpace.ingredientsText[0]+' "Ingredient#1" / 100ml')
        self.lbl2.setText(sharedSpace.ingredientsText[1]+' "Ingredient#2" / 100ml')
        self.lbl3.setText(sharedSpace.ingredientsText[2]+' "Ingredient#3" / 100ml')
        self.lbl4.setText(sharedSpace.ingredientsText[3]+' "Ingredient#4" / 100ml')
        self.selectedD=(sharedSpace.getSelectedDrink())-1
        self.ql1.setText(sharedSpace.drinkNames[ self.selectedD])
        self.ql2.setText(str(sharedSpace.drinksIngredientsMl[self.selectedD][0]))
        self.ql3.setText(str(sharedSpace.drinksIngredientsMl[self.selectedD][1]))
        self.ql4.setText(str(sharedSpace.drinksIngredientsMl[self.selectedD][2]))
        self.ql5.setText(str(sharedSpace.drinksIngredientsMl[self.selectedD][3]))

        
        self.TimerClock = QTimer()
        self.TimerClock.setInterval(1000)#Refresh the game timer after every 1 second=1 milliseconds
        self.TimerClock.timeout.connect(self.ClockTimer)
        self.TimerClock.start()
    def openKeyboard(self):
        print('opening/closing keyboard')
        shellscript=subprocess.Popen(['sh', './keyboardToggle.sh'], stdin=subprocess.PIPE)
    def getfile(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file',  'c:\\',"Image files (*.jpg *.png)")
        print(fname)
        if(fname!='' and fname!=None):
            dn=sharedSpace.selectedDrink
            mk=dn.split(';')
            m=int(mk[1])
            self.ql1.setText(sharedSpace.drinkNames[m-1])
            sharedSpace.drinksPath[m-1]=fname[0]
            

    def clkB1(self):
        print('B1')
        dn=sharedSpace.selectedDrink
        mk=dn.split(';')
        m=int(mk[1])
        sharedSpace.drinksIngredientsMl[m-1][0]=self.ql2.text()
        sharedSpace.drinksIngredientsMl[m-1][1]=self.ql3.text()
        sharedSpace.drinksIngredientsMl[m-1][2]=self.ql4.text()
        sharedSpace.drinksIngredientsMl[m-1][3]=self.ql5.text()

        sharedSpace.drinkNames[m-1]=self.ql1.text()

        sharedSpace.saveSettings()
        sharedSpace.requestUpdate(0)
        sharedSpace.requestUpdate(1)
        self.hide()

    def clkB2(self):
        print('B2')
        self.hide()

    def clkB3(self):
        print('B3')
        self.getfile()


    def loadFile(self):
        print('loadfile')
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
        print('loadui')
        #laods the answer screen and applies the theme
        path = os.path.join(os.path.dirname(__file__), "ansSheet.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.win=loader.load(ui_file, self)
        #win.show()
        ui_file.close()

