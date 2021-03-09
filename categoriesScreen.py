#This is the categories screen
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

from ansSheet import *

from pyside_material import apply_stylesheet
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

class CategoriesWindow(QtWidgets.QWidget):
    """
    This "window" is a QWidget. If it has no parent, it 
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        #QtWidgets.QWidget.__init__(self)
        

        super(CategoriesWindow, self).__init__()

        self.timerVal=0
        



        self.ansWindow = AnsSheet()
        

        self.screenActivate=0
        self.screenANum=0

        self.selectionV=[0,0] #this is a main array which stores the selections
        
        self.setWindowTitle('Categories')
        
        
        
        self.load_ui()
        self.center()    
        self.selectedD=(sharedSpace.getSelectedDrink())-1

        #all categores and amount buttons below
        self.b1 = self.findChild(QtWidgets.QPushButton, "b1")
        self.b2 = self.findChild(QtWidgets.QPushButton, "b2")
        self.b3 = self.findChild(QtWidgets.QPushButton, "b3")
        
        self.lb1 = self.findChild(QtWidgets.QPushButton, "lb1")

        self.bck = self.findChild(QtWidgets.QLabel, "bck")
        clickable(self.bck).connect(self.backScr)

        self.il1 = self.findChild(QtWidgets.QLabel, "il1")
        self.il2 = self.findChild(QtWidgets.QLabel, "il2")
        self.il3 = self.findChild(QtWidgets.QLabel, "il3")
        self.il4 = self.findChild(QtWidgets.QLabel, "il4")
        self.dn = self.findChild(QtWidgets.QLabel, "dn")
        g=int((sharedSpace.selectedDrink.split(';'))[1])
        self.dn.setText(sharedSpace.drinkNames[g-1])

        self.il1.setText(sharedSpace.ingredientsText[0]+' '+str(sharedSpace.drinksIngredientsMl[self.selectedD][0]))
        self.il2.setText(sharedSpace.ingredientsText[1]+' '+str(sharedSpace.drinksIngredientsMl[self.selectedD][1]))
        self.il3.setText(sharedSpace.ingredientsText[2]+' '+str(sharedSpace.drinksIngredientsMl[self.selectedD][2]))
        self.il4.setText(sharedSpace.ingredientsText[3]+' '+str(sharedSpace.drinksIngredientsMl[self.selectedD][3]))
        
        self.lb1 = self.findChild(QtWidgets.QLabel, "lb1")

        self.r1l = self.findChild(QtWidgets.QLabel, "r1l")
        self.r2l = self.findChild(QtWidgets.QLabel, "r2l")
        self.r3l = self.findChild(QtWidgets.QLabel, "r3l")

        self.r1 = self.findChild(QtWidgets.QLabel, "r1")
        self.r2 = self.findChild(QtWidgets.QLabel, "r2")
        self.r3 = self.findChild(QtWidgets.QLabel, "r3")
        self.r1.setText('')
        self.r2.setText('')
        self.r3.setText('')
        self.checkBoxChecked= QtGui.QPixmap('img/checkbox_checked.png')
        self.checkBoxUnChecked= QtGui.QPixmap('img/checkbox_unchecked.png')
        self.r1.setPixmap(self.checkBoxChecked)
        self.r2.setPixmap(self.checkBoxUnChecked)
        self.r3.setPixmap(self.checkBoxUnChecked)
        clickable(self.r1).connect(self.cb1)
        clickable(self.r2).connect(self.cb2)
        clickable(self.r3).connect(self.cb3)

        

        self.juice =[ QtGui.QPixmap(sharedSpace.drinksPath[self.selectedD])]
        self.backImg= QtGui.QPixmap('img/back.png')

        # self.lb1.setStyleSheet("QLabel::hover"
        #                                     "{"
        #                                         "background-color : rgb(232, 243, 193);"
        #                                     "}") 
        # self.bck.setStyleSheet("QLabel::hover"
        #                                     "{"
        #                                         "background-color : rgb(232, 243, 193);"
        #                                     "}") 

        
        self.lb1.setPixmap(self.juice[0])
        self.bck.setPixmap(self.backImg)


        self.b1.clicked.connect(self.clkB1)
        self.b2.clicked.connect(self.clkB2)
        self.b3.clicked.connect(self.clkB3)


        self.UITimer = QTimer()
        self.UITimer.setInterval(1200)# refresh the screen after every 1.2 seconds(1.2 instead of 1 is to avoid the conflict with other screens)
        self.UITimer.timeout.connect(self.UIMethod)
        self.UITimer.start()
    def cb1(self):
        self.r1.setPixmap(self.checkBoxChecked)
        self.r2.setPixmap(self.checkBoxUnChecked)
        self.r3.setPixmap(self.checkBoxUnChecked)
        sharedSpace.selectedMl=1
    def cb2(self):
        self.r1.setPixmap(self.checkBoxUnChecked)
        self.r2.setPixmap(self.checkBoxChecked)
        self.r3.setPixmap(self.checkBoxUnChecked)
        sharedSpace.selectedMl=2
        
    def cb3(self):
        self.r1.setPixmap(self.checkBoxUnChecked)
        self.r2.setPixmap(self.checkBoxUnChecked)
        self.r3.setPixmap(self.checkBoxChecked)
        sharedSpace.selectedMl=3
        
    def UIMethod(self):
        #checks screen change event
        if(self.screenActivate==1):
            if(self.screenANum==1):
                self.toggle_window(self.ansWindow,'ans')
            self.screenActivate=0
            self.screenANum=0

    def catBtnSelection(self, btnName, sel):
        #
        if(sel==True):
            
            for i in range(0,5):
                if(i!=btnName):
                    a=0 #just a place holder for future use
                   
        else:
            a=0 #just a place holder for future use
            
    def backScr(self):
        print('back')
        self.hide()
        sharedSpace.activeWindow="main"
    def clkB1(self):
        #this function handles button press using mouse which is not used
        print("clicked 1")
        
        print(sharedSpace.selectedMl)

        print('sharedSpace;;;',sharedSpace.selectedDrink)
        #self.lb1.move(self.b1.pos().x()+60,self.b1.pos().y()+50)
    def clkB2(self):
        #this function handles button press using mouse which is not used
        print("clicked 2")
        #self.lb1.move(self.b2.pos().x()+60,self.b2.pos().y()+50)
    def clkB3(self):
        #this function handles button press using mouse which is not used
        print("clicked 3")
        self.screenActivate=1
        self.screenANum=1
        self.UIMethod()
        #self.toggle_window(self.ansWindow,'ans')

            

    def toggle_window(self, window,winName):
        #hanldes current screen open/close events
        if(winName=='ans'):
            if (window.isVisible()):
                window.hide()
            else:
                
                self.ansWindow = AnsSheet()
               
                apply_stylesheet(self.ansWindow, theme='dark_blue.xml')
               
                
                self.ansWindow.showFullScreen()

        elif(winName=='ans'):
            if (window.isVisible()):
                window.hide()
            else:
                
                self.ansWindow = AnsSheet()
            
                apply_stylesheet(self.ansWindow, theme='dark_blue.xml')
                sharedSpace.catVals[0]=self.selectionV[0]
                sharedSpace.catVals[1]=self.selectionV[1]
                
                self.ansWindow.showFullScreen()
    
    def center(self):
            
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # move rectangle's 
    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "categories.ui")
        print(path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        win=loader.load(ui_file, self)
        self.center()
        #win.show()
        
        ui_file.close()