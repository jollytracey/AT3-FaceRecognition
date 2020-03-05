import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import shutil
from resizeScript import *
from FlickrDAL import FlickrDAL
class AddIdWidget(QWidget):
 
    def __init__(self,parent):
        assert isinstance(parent,QStackedWidget)
        super(AddIdWidget,self).__init__()
        self.title = 'Add ID Images '
        self.left = 100
        self.top = 100
        self.width = 300    
        self.height = 300
        self.url=""
        self.name=""
        self.parent=parent
        self.initUI()
 
    def initUI(self):
        vbox=QVBoxLayout()
        hbox1=QHBoxLayout()
        hbox2=QHBoxLayout()
        hbox3=QHBoxLayout()
        #first line
        btnBrowse=QPushButton("Browse for ID picture:")
        btnBrowse.clicked.connect(self.selectImage)
        #btnBrowse.resize(btnBrowse.sizeHint())
        #btnBrowse.move(50,50)
        self.urllabel = QLabel("")
        hbox1.addWidget(btnBrowse)
        hbox1.addWidget(self.urllabel)
        #second line
        l=QLabel("Who is this?:")
        self.inputField=QLineEdit()
        hbox2.addWidget(l)
        hbox2.addWidget(self.inputField)
        #third line
        ok=QPushButton("Import image")
        ok.clicked.connect(self.submit)
        back=QPushButton("Back to main screen")
        back.clicked.connect(self.back)
        hbox3.addWidget(ok)
        hbox3.addWidget(back)
        #outer layout
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #self.show()
    def selectImage(self):
        self.url,filter=QFileDialog.getOpenFileName(self,'Select image','/media/pi','(*.jpeg *.jpg *.png *.bmp)')
        print(self.url)
        self.urllabel.setText(self.url)
        
        self.name=os.path.splitext(os.path.basename(self.url))[0]
        self.ext=os.path.splitext(os.path.basename(self.url))[1]
        self.inputField.setText(self.name)
        print(self.ext)
        pass

    def submit(self):
        name=self.inputField.text()
        dest=os.getcwd()+"/users/{}".format(name+self.ext)
        shutil.copy2(self.url,dest)
        resizeImage()
        FlickrDAL().insertUser(name)
        os.remove(os.getcwd()+"\tag")
        os.remove(os.getcwd()+"\enc")
        #going back
        self.back()
        pass
    def back(self):
        self.parent.setCurrentIndex(0)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AddIdWidget()
    sys.exit(app.exec_())
