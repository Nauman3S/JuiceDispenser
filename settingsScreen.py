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
        self.txtBoxes=[self.txt1,self.txt2,self.txt3,self.txt4]
        clickable(self.txt1).connect(self.text1Click)
        clickable(self.txt2).connect(self.text2Click)
        clickable(self.txt3).connect(self.text3Click)
        clickable(self.txt4).connect(self.text4Click)
        self.SelectedTXTBox=1

        self.b2.clicked.connect(self.clkB2)
        self.b3.clicked.connect(self.clkB3)

        self.txt1.setText(sharedSpace.ingredientsText[0])
        self.txt2.setText(sharedSpace.ingredientsText[1])
        self.txt3.setText(sharedSpace.ingredientsText[2])
        self.txt4.setText(sharedSpace.ingredientsText[3])
        
        self.KeyboardState=False
        self.CapsOn=True
        self.keyboardLayout= self.findChild(QtWidgets.QFrame,'kayboardLayout')
        self.keyboardLayout.setVisible(False)
        self.KeyCaps=self.findChild(QtWidgets.QPushButton,"KeyCaps")
        self.KeyCaps.clicked.connect(self.capsBtn)
        self.KeySpace=self.findChild(QtWidgets.QPushButton,"KeySpace")
        self.KeySpace.clicked.connect(self.spaceBtn)
        self.keys=['A','S','D','F','G','H','J','K','L','Q','W','E','R','T','Y','U','I','O','P','Z','X','C','V','B','N','M']
        
        self.NumberKeys=[]
        self.CharKeys=[]
        for i in range(0,10):
            self.NumberKeys.append(self.findChild(QtWidgets.QPushButton, "Key"+str(i)))
           
            #print(i)
        
        self.NumberKeys[0].clicked.connect(lambda: self.numKeysBtn(str(0)))
        self.NumberKeys[1].clicked.connect(lambda: self.numKeysBtn(str(1)))
        self.NumberKeys[2].clicked.connect(lambda: self.numKeysBtn(str(2)))
        self.NumberKeys[3].clicked.connect(lambda: self.numKeysBtn(str(3)))
        self.NumberKeys[4].clicked.connect(lambda: self.numKeysBtn(str(4)))
        self.NumberKeys[5].clicked.connect(lambda: self.numKeysBtn(str(5)))
        self.NumberKeys[6].clicked.connect(lambda: self.numKeysBtn(str(6)))
        self.NumberKeys[7].clicked.connect(lambda: self.numKeysBtn(str(7)))
        self.NumberKeys[8].clicked.connect(lambda: self.numKeysBtn(str(8)))
        self.NumberKeys[9].clicked.connect(lambda: self.numKeysBtn(str(9)))

        #print(self.NumberKeys)
        for i in range(0,len(self.keys)):
            self.CharKeys.append(self.findChild(QtWidgets.QPushButton, "Key"+self.keys[i]))
            # self.CharKeys[i].clicked.connect(lambda: self.charKeysBtn(self.keys[i]))

        self.loadStates()
        # print(self.CharKeys)

        self.CharKeys[0].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[0].text()))
        self.CharKeys[1].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[1].text()))
        self.CharKeys[2].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[2].text()))
        self.CharKeys[3].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[3].text()))
        self.CharKeys[4].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[4].text()))
        self.CharKeys[5].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[5].text()))
        self.CharKeys[6].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[6].text()))
        self.CharKeys[7].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[7].text()))
        self.CharKeys[8].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[8].text()))
        self.CharKeys[9].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[9].text()))
        self.CharKeys[10].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[10].text()))
        self.CharKeys[11].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[11].text()))
        self.CharKeys[12].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[12].text()))
        self.CharKeys[13].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[13].text()))
        self.CharKeys[14].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[14].text()))
        self.CharKeys[15].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[15].text()))
        self.CharKeys[16].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[16].text()))
        self.CharKeys[17].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[17].text()))
        self.CharKeys[18].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[18].text()))
        self.CharKeys[19].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[19].text()))
        self.CharKeys[20].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[20].text()))
        self.CharKeys[21].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[21].text()))
        self.CharKeys[22].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[22].text()))
        self.CharKeys[23].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[23].text()))
        self.CharKeys[24].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[24].text()))
        self.CharKeys[25].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[25].text()))
    #the functions below handles the mouse click events 
    def text1Click(self):
        print('txt1 clicked')
        self.keyboardLayout.setVisible(True)
        self.keyboardLayout.move(20,270)
        self.SelectedTXTBox=1
    def text2Click(self):
        print('txt2 clicked')
        self.keyboardLayout.setVisible(True)
        self.keyboardLayout.move(20,270)
        self.SelectedTXTBox=2
    def text3Click(self):
        print('txt3 clicked')
        self.SelectedTXTBox=3
        self.keyboardLayout.setVisible(True)
        self.keyboardLayout.move(20,80)
    def text4Click(self):
        print('txt4 clicked')
        self.keyboardLayout.setVisible(True)
        self.keyboardLayout.move(20,80)
        self.SelectedTXTBox=4
    def spaceBtn(self):
        txt=self.txtBoxes[self.SelectedTXTBox-1].text()
        self.txtBoxes[self.SelectedTXTBox-1].setText(txt+' ')

    def capsBtn(self):
        print('caps pressed')
        # self.CharKeys[0].setText('a')
        self.CapsOn=not(self.CapsOn)

        # if(self.CapsOn):
        #     self.CharKeys[0].setText(self.keys[0].lower())
                
        # else:
           
        #     self.CharKeys[0].setText(self.keys[0].upper())
        # self.CapsOn=not(self.CapsOn)
        # self.update()

    
    def numKeysBtn(self,btn):
        print('pressed:::',btn)
        
        txt=self.txtBoxes[self.SelectedTXTBox-1].text()
        self.txtBoxes[self.SelectedTXTBox-1].setText(txt+str(btn))
    def charKeysBtn(self,btn):
        print('pressed:::',btn)
        txt=self.txtBoxes[self.SelectedTXTBox-1].text()
        if(self.CapsOn):
            self.txtBoxes[self.SelectedTXTBox-1].setText(txt+str(btn).upper())
        else:
            self.txtBoxes[self.SelectedTXTBox-1].setText(txt+str(btn).lower())

    def openKeyboard(self):

        print('opening/closing keyboard')
        #shellscript=subprocess.Popen(['sh', './keyboardToggle.sh'], stdin=subprocess.PIPE)
        # self.KeyboardState=not (self.KeyboardState)
        if(self.KeyboardState):
            self.KeyboardState=False
            self.keyboardLayout.setVisible(self.KeyboardState)
            
        else:
            self.KeyboardState=True
            self.keyboardLayout.setVisible(self.KeyboardState)
            

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
