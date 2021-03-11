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
        self.txtBoxes=[self.ql1,self.ql2,self.ql3,self.ql4,self.ql5]
        clickable(self.ql1).connect(self.text1Click)
        clickable(self.ql2).connect(self.text2Click)
        clickable(self.ql3).connect(self.text3Click)
        clickable(self.ql4).connect(self.text4Click)
        clickable(self.ql5).connect(self.text5Click)

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

        # self.loadStates()
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

        
        self.TimerClock = QTimer()
        self.TimerClock.setInterval(1000)#Refresh the game timer after every 1 second=1 milliseconds
        self.TimerClock.timeout.connect(self.ClockTimer)
        self.TimerClock.start()
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
    def text5Click(self):
        print('txt5 clicked')
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

