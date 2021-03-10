#This is settings screen main file
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
import sharedSpace
import time
import subprocess
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
class SettingsWindow(QtWidgets.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        #os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard" # Import virtual keyboard
        self.qtVal=0 #Question timer selected value
        self.ddVal=0 #daily double selected value
        self.fjVal=0 #final jeopardy selected value
        self.timerVal=0 
        self.setWindowTitle('Settings')
        
        self.load_ui()
        self.center()    
        sharedSpace.loadSettings()
        #Image files for selected and unselected buttons are defined below
        self.pixmapOFF =[ QtGui.QPixmap('off0.png'),QtGui.QPixmap('on0.png'),QtGui.QPixmap('sec5.png'),QtGui.QPixmap('sec10.png')]
        self.pixmapON = [ QtGui.QPixmap('off1.png'),QtGui.QPixmap('on1.png'),QtGui.QPixmap('sec5on.png'),QtGui.QPixmap('sec10on.png')]

        self.keyboardIcon=QtGui.QPixmap(sharedSpace.keyboardICO)
        self.keyboard= self.findChild(QtWidgets.QLabel,'keyboard')
        self.keyboard.setPixmap(self.keyboardIcon)
        clickable(self.keyboard).connect(self.openKeyboard)

        self.b2 = self.findChild(QtWidgets.QPushButton, "b2")
        self.b3 = self.findChild(QtWidgets.QPushButton, "b3")

        self.lb_2_1 = self.findChild(QtWidgets.QLabel, "lb1")
        self.lb_2_2 = self.findChild(QtWidgets.QLabel, "lb2")
        self.lb_2_3 = self.findChild(QtWidgets.QLabel, "lb3")

        self.lb_2_4 = self.findChild(QtWidgets.QLabel, "lb4")
        self.lb_2_5 = self.findChild(QtWidgets.QLabel, "lb5")

        self.lb_2_6 = self.findChild(QtWidgets.QLabel, "lb6")
        self.lb_2_7 = self.findChild(QtWidgets.QLabel, "lb7")


        self.txt1 = self.findChild(QtWidgets.QLineEdit, "txt1")
        self.txt2 = self.findChild(QtWidgets.QLineEdit, "txt2")
        self.txt3 = self.findChild(QtWidgets.QLineEdit, "txt3")
        self.txt4 = self.findChild(QtWidgets.QLineEdit, "txt4")
        
        self.b2.clicked.connect(self.clkB2)
        self.b3.clicked.connect(self.clkB3)

        self.txt1.setText(sharedSpace.ingredientsText[0])
        self.txt2.setText(sharedSpace.ingredientsText[1])
        self.txt3.setText(sharedSpace.ingredientsText[2])
        self.txt4.setText(sharedSpace.ingredientsText[3])

        self.loadStates()
       
    #the functions below handles the mouse click events 
    def openKeyboard(self):

        print('opening/closing keyboard')
        shellscript=subprocess.Popen(['sh', './keyboardToggle.sh'], stdin=subprocess.PIPE)
    def clkB2(self):
        print("b2")
        sharedSpace.ingredientsText[0]=self.txt1.text()
        sharedSpace.ingredientsText[1]=self.txt2.text()
        sharedSpace.ingredientsText[2]=self.txt3.text()
        sharedSpace.ingredientsText[3]=self.txt4.text()
        sharedSpace.saveSettings()
        sharedSpace.requestUpdate(1)
        self.hide()
    def clkB3(self):
        print("b3")
        self.hide()
    
    

    def btnSelections(self,sel):
        print('no')
   
    def writeStates(self,statesList):
        # save all settings to a settings.conf file
        m=open("settings.conf",'w')
        m.write(statesList[0]+","+statesList[1]+","+statesList[2])
        print("writer")
        m.close()
    def loadStates(self):
        #open the saved settings from settings.conf file and display the button states accordingly
        g=open("settings.conf",'r')
        mk=g.read()
        g.close()
        mv=mk.split(",")
        print(mv)
        if(mv[0]=="0"):
            self.btnSelections("qtoff")
            self.qtVal=0
            self.timerVal=0
        if(mv[0]=="1"):
            self.btnSelections("qt5sec")
            self.qtVal=1
            self.timerVal=5
        if(mv[0]=="2"):
            self.btnSelections("qt10sec")
            self.qtVal=2
            self.timerVal=10
        if(mv[1]=="0"):
            self.btnSelections("ddoff")
            self.ddVal=0
        if(mv[1]=="1"):
            self.btnSelections("ddon")
            self.ddVal=1
        if(mv[2]=="0"):
            self.btnSelections("fjoff")
            self.fjVal=0
        if(mv[2]=="1"):
            self.btnSelections("fjon")
            self.fjVal=1

                
            
    def buttonSelection(self, btnName, sel):
        # handle buttons theme
        if(sel==True):
            btnName.setStyleSheet("QPushButton{ background-color: rgb(91,187,122); color: rgb(0, 0, 0);}")
        else:
            btnName.setStyleSheet("QPushButton{ background-color: rgb(49,54,59); color: rgb(66, 132, 242);}")
    def center(self):
            
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # move rectangle's 
    def load_ui(self):
        #main loader
        path = os.path.join(os.path.dirname(__file__), "settings.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        win=loader.load(ui_file, self)
        win.showFullScreen()
        
        ui_file.close()
