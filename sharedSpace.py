#this file stores the shared variables
import ast
drinkNames=['Half-Orange', 'Orange Water', 'Organic Orange', 'Mint Lemonade', 'Blueberry Dose','Raspberry Extract']
selectedDrink="D;1"
activeWindow="main"

ingredientsText=['Gin', 'Lemon', 'Malt','Orange']

drinksPath=['drinks/1.png','drinks/2.png','drinks/3.png','drinks/4.png','drinks/5.png','drinks/6.png']
keyboardICO='img/keyboard.png'

drinksIngredientsMl=[[20,10,10,10],[20,10,10,10],[20,10,10,10],[20,10,10,10],[20,10,10,10],[20,10,10,10]]

selectedMl=1

updateNow=[0,0,0]

def getSelectedDrink():
    global selectedDrink
    m=selectedDrink.split(';')
    km=int(m[1])
    return km
def updatePics(scr):
    global updateNow
    if(updateNow[scr]==1):
        updateNow[scr]=0
        return 1
    
def requestUpdate(scr):
    global updateNow
    updateNow[scr]=1

def saveSettings():
    global drinkNames,ingredientsText,drinksPath, drinksIngredientsMl
    g=open('settings.conf','w')
    g.write(str(drinkNames)+';'+str(ingredientsText)+';'+str(drinksPath)+';'+str(drinksIngredientsMl))
    g.close()
def loadSettings():
    global drinkNames,ingredientsText,drinksPath,drinksIngredientsMl
    m=open('settings.conf','r')
    k=m.read()
    m.close()
    gg=k.split(';')
    drinkNames=ast.literal_eval(gg[0])
    ingredientsText=ast.literal_eval(gg[1])
    drinksPath=ast.literal_eval(gg[2])
    drinksIngredientsMl=ast.literal_eval(gg[3])
    

# saveSettings()
# loadSettings()

# print(drinkNames,ingredientsText,drinksPath,drinksIngredientsMl)