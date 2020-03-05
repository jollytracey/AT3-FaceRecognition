from itertools import cycle
from PIL import Image, ImageTk
import os
import ctypes
import time
from FlickrService import *
import random
import pickle
#import threading

from multiprocessing import Process, Lock, Queue
from collections import deque
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
class SlideShowApp(Process):
    '''Tk window/label adjusts to size of image'''
    def __init__(self, folderList=[], delay=3000,lock=Lock()):
        self.folderList=set(folderList)
        self.delay=delay
        self.lock=lock
        self.prevSet=set()
        Process.__init__(self)
        
    def run(self):
        self.initialize(self.folderList,self.delay)
        
    def callback(self):
        self.root.quit()
        
    def initialize(self,folderList,delay):
        #tk.Tk.__init__(self)
        self.root=tk.Tk()
        self.okToQuit=False
        # set x, y position only
        #self.geometry('+{}+{}'.format(x, y))
        self.root.attributes("-fullscreen", True)
        self.image_files=[]
        #self.setup(folderList)
        # allows repeat cycling through the pictures
        self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files) if len(self.image_files)!=0 else []
        self.picture_display = tk.Label(self.root, bd=0,fg="red",font=("Courier",44))
        self.root.bind('<Button-1>',self.stop)
        self.picture_display['text']="Loading components.\n Please wait"
        self.picture_display.pack()
        self.root.configure(background='black')
        print("resolution:",(self.root.winfo_screenwidth(),self.root.winfo_screenheight()))
        self.root.after(1000*30*60, self.ImportFromFlickr)
        self.show_slides()
        self.root.mainloop()
        self.isstop=False
        
    def show_slides(self):
        '''cycle through the images and show them'''
        #self.lock.acquire()
        #print('calling showslides with newperson'+str(self.newPerson.qsize()))
        if (self.newPerson.qsize())!=0:
            while self.newPerson.qsize()>0:
                try:
                    something=self.newPerson.get()
                    if something[0]=="#": # "#" denotes an incoming message
                       self.picture_display['text']=something[1:]
                       self.okToQuit=True
                    else: #something is the folder name list
                        #self.picture_display.config(image='')
                        #self.picture_display['text']="{} found. Loading {}'s album".format(something)
                        
                        self.addFolder(something)
                except:
                    break
            #self.setup(self.folderList)
            self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files) if len(self.image_files)!=0 else []
        if len(self.image_files)==0:
            self.root.after(self.delay, self.show_slides)
            return
        img_object= next(self.pictures) 
        self.picture_display.config(image=img_object)
        self.root.after(self.delay, self.show_slides)
        #self.lock.release()
    def clone(self):
        _clone=SlideShowApp(self.folderList,self.delay,self.lock)
        return _clone
    def stop(self,event):
        if not self.okToQuit:
            return
        self.root.destroy()
        self.exitQueue.put("x")
        
    def startSlideShow(self):
        self.start()
        
    def addFolder(self,folderList):
        #self.folderList.add(folder)
        self.setup(folderList)
        #self.setup(self.folderList)
        #self.pictures = cycle(ImageTk.PhotoImage(image) for image in self.image_files)
        
    def setup(self,folderList):
        """"folderList contains the img file name"""
        try:
            if len(folderList)==0:
                return
            width,height=self.root.winfo_screenwidth(),self.root.winfo_screenheight()
            
            path=os.getcwd()+"/FlickrPhotos"
            nameset=set(folderList)
            if nameset==self.prevSet:
                return
            if not os.path.exists(path):
                os.mkdir(path)
                return
            self.image_files=[]
            print("Importing photos for this set")
            print(folderList)
            #add the images to a list
            for file_name in folderList:                
                subpath=path+"/"+file_name
                if not os.path.exists(subpath):
                    continue
                raw_image=Image.open(subpath)
                iwidth,iheight=raw_image.size
                scalew=height/iheight
                #scale the image along the height of the monitor
                iheight=height
                iwidth=int(iwidth*scalew)
                #resizing the image to current resolution
                self.image_files.append(raw_image.resize((iwidth,iheight), Image.BILINEAR))
                    
                pass
            
            self.shuffleImages()
            pass
        except Exception as e:
            print(e)
    def shuffleImages(self):
        random.shuffle(self.image_files)
        pass
                    
    def ImportFromFlickr(self):
        downloadPhotos()
        #p=Process(target=downloadPhotos)
        #p.start()
        import customFaceRec
        p=Process(target=customFaceRec.tag)
        p.start()
        self.root.after(1000*30, self.ImportFromFlickr)
        

def main():
    
    
    app = SlideShowApp()
    app.newPerson=Queue()
    app.exitQueue=Queue()
    app.start()
    #from customFaceRec import RecognizeScript
    #s=RecognizeScript(app)
    #s.start()
    #s.join()
    
    
    #run_face_rec(app) #running face recognition will populate the lis of recognizable persons
    app.join()
    #app.terminate()
    #app.start()
if __name__ == "__main__":
    main()
    
