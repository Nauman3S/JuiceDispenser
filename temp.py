#temporary test file
import sys
import os


b=[1,1,1,1]

print(all(v == 1 for v in b))
#path = os.path.join(os.path.dirname(__file__), "data\\"+"cat"+str(i)+"_"+str(j))
#print("\n\n\n\n"+path+'\n\n\n\n')

# for i in range(0,5):
#     for j in range(0,6):
#         path = os.path.join(os.path.dirname(__file__), "data","cat"+str(i+1)+"_"+str(j+1)+'.txt')
#         g=open(path,'w')
#         g.write("ANSWER NUMBER "+str(i+1)+"_"+str(j+1))
#         g.close()


def genFilesList():
    l1=[0,0,0,0,0,0]
    lst=[l1,l1,l1,l1,l1]
    print(lst)
    for i in range(0,5):
        for j in range(0,6):
            lst[i][j]="cat"+str(i+1)+"_"+str(j+1)+'.txt'

    print(lst)

genFilesList()

g=('C:/Users/nauma/OneDrive/Pictures/px100.png', 'Image files (*.jpg *.png)')
print(g[0])
import sys, os
from PySide2.QtWidgets import QApplication, QLineEdit
                                                     
if __name__ == "__main__":
    os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard" # Import virtual keyboard
    app = QApplication(sys.argv)
    lineEdit = QLineEdit()
    lineEdit.show()
    sys.exit(app.exec_())