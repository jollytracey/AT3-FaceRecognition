from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import shutil
import os, sys
from multiprocessing import Process, Lock, Queue
from AddIDWindow import *
from FlickrService import *
class At3(QStackedWidget):
    
    def __init__(self):
        super(At3, self).__init__()
        self.main=QWidget()
        self.addId=AddIdWidget(self)
        self.initUI()
        self.addWidget(self.main) #0
        self.addWidget(self.addId) #1
        self.encodings={}
        self.showFullScreen()
        self.count=0
        
        
    def initUI(self):
        #self.setGeometry(10, 10, 800, 400)
        self.setWindowTitle('AT3') 
        vbox=QVBoxLayout()
        size=QtWidgets.QDesktopWidget().screenGeometry(-1)
        print('{}*{}'.format(size.width(),size.height()))
        self.width,self.height=size.width(),size.height()
        #---add some color----

        #------
        btnAdd = QPushButton('Add ID photos', self)
        #btnAdd.resize(btnAdd.sizeHint())
        btnAdd.clicked.connect(self.AddImageID)
        #btnAdd.move(self.width*9/20, self.height*20/100)  

        btnRun= QPushButton('Start Slideshow', self)
        #btnRun.resize(btnRun.sizeHint())
        btnRun.clicked.connect(self.slideshow)
        #btnRun.move(self.width*9/20, self.height*30/100)  

        #btnAddF= QPushButton('Add Flickr Account', self)
        #btnAddF.resize(btnAddF.sizeHint())
        #btnAddF.clicked.connect(self.AddFlickrAcc)
        #btnAddF.move(self.width*9/20, self.height*40/100)
        
        btnExit = QPushButton('Exit', self)
        #btnExit.resize(btnExit.sizeHint())
        btnExit.clicked.connect(self.Exit)
        #btnExit.move(self.width*9/20, self.height*50/100)  
        vbox.addWidget(btnAdd)
        vbox.addWidget(btnRun)
        #vbox.addWidget(btnAddF)
        vbox.addWidget(btnExit)
        self.main.setLayout(vbox)
        

        #self.show()

    def Exit(self):
        exit()
        
    def AddFlickrAcc(self):
        #TO-DO
        pass
    
    def slideshow(self):
        """Initialize the slideshow"""
        if len(self.encodings)==0:
            from slideshow import SlideShowApp
        app = SlideShowApp()
        app.newPerson=Queue()
        app.exitQueue=Queue()
        app.start()
        downloadPhotos()
        #from customFaceRec import RecognizeScript
        #s=RecognizeScript(app)
        #s.start()
        #s.join()
        if len(self.encodings)==0:
            import customFaceRec
        #customFaceRec.tag()
        p=Process(target=customFaceRec.run_face_rec, args=(app,))
        self.count+=1
        p.start()
        p.join()
        
        #run_face_rec(app) #running face recognition will populate the lis of recognizable persons
        app.join()
        
        #slideshow.main()
        pass
    def AddImageID(self):
        
        self.setCurrentIndex(1)
        # resize images in ~/users folder    
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = At3()
    sys.exit(app.exec_())
