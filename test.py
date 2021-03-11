
k='self.CharKeys[0].clicked.connect(lambda: self.charKeysBtn(self.CharKeys[0].text()))'

for i in range(0,26):
    print('self.CharKeys['+str(i)+'].clicked.connect(lambda: self.charKeysBtn(self.CharKeys['+str(i)+'].text()))')


a="asd"
a=a[:-1]
print(a)