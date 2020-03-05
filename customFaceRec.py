
# To run this, you need a Raspberry Pi 2 (or greater) with face_recognition and
# the picamera[array] module installed.
# You can follow this installation instructions to get your RPi set up:
# https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

import face_recognition
import picamera
import numpy as np
import os
from multiprocessing import Process
import time
import shutil
import pickle


def writeLastModified(lines):
    fh=open('id_track.txt','w')
    fh.writelines(lines)
    fh.close()
def readLastModified():
    fh=open('id_track.txt','r')
    lm={}
    for line in fh:
        name,date=line.split('|')[0],line.split('|')[1][:-1]
        lm[name]=date
    fh.close()
    return lm
def deleteFlickr():
    print("Deleting all photos from Flickr....")
    path=os.getcwd()+"/FlickrPhotos"
    for f in os.listdir(path):
        os.remove(path+"/"+f)
    print("Done")
def readEncodings(path=os.getcwd()+"/users"):
    # Load a sample picture and learn how to recognize it.
    print("Loading known face image(s)")
    if os.path.exists(os.getcwd()+"/enc"):
        h=None
        with open("enc","rb") as f:
            h=pickle.load(f)
        return h
    known_encodings=None
    #----------------reading from "users" folder-------------------------
    known_encodings={}
    #print(path)
    imgFileExt=("gif","jpg","jpeg","png")
    filelist=[files for r,dirs,files in os.walk(path,topdown=True)][0] #get the list of all files
    imgList=[]
    #Select the file with name that like this "_abc.jpeg"
    lm=readLastModified()
    #print(lm)
    #print(filelist)
    #print(known_encodings.keys())
    lines_to_write=[]
    for file in filelist:
        #check if file is image and in the right format
        if file.lower().endswith(imgFileExt) and file[0]=="_":
            #check if new file or file has changed
            person=file[1:file.find(".")]
            if file not in lm or str(os.path.getmtime(path+'/'+file))!=lm[file] or (person not in known_encodings):   
                imgList.append(file)
            lines_to_write.append(file +"|"+ str(os.path.getmtime(path+'/'+file))+"\n")
    print(imgList)
    #-------------------loading faces---------------------
    for filename in imgList:
        person=filename[1:filename.find(".")]
        print("Generating encodings for "+person)
        face_encoding=face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+filename))[0]
        known_encodings[person]=face_encoding
    #-----write to a file------
    with open("enc","wb") as f:
        pickle.dump(known_encodings,f)
    return known_encodings

def tag(threshold=0.50):
    h={}
    if os.path.exists(os.getcwd()+"/tag"):
        with open("tag","rb") as f:
            h=pickle.load(f)
    """tag the images with names on it"""
    #if known_encodings==None:
    #    known_encodings=readEncodings()
    print("Begin tagging photos....")
    flickrdir=os.getcwd()+"/FlickrPhotos"
    filelist=os.listdir(flickrdir)
    #scroll through each pictures
    for filename in filelist:
        if filename in h:
            continue
        ext= filename[filename.rfind("."):]
        #get the list of encodings from img
        inputImg=face_recognition.load_image_file(flickrdir+"/"+filename)
        face_loc=face_recognition.face_locations(inputImg)
        img_face_encodings=face_recognition.face_encodings(inputImg, face_loc,2)
        h[filename]=img_face_encodings
        print("Done tagging %s"%(filename))
    with open("tag","wb") as f:
        pickle.dump(h,f)
    #scroll through the encodings
    return h
    pass



def run_face_rec(app=None):
    path=os.getcwd()+"/users"
    # Get a reference to the Raspberry Pi camera.
    # If this fails, make sure you have a camera connected to the RPi and that you
    # enabled your camera in raspi-config and rebooted first.
    width,height=320,240 #320,240 by default
    camera = picamera.PiCamera()
    camera.resolution = (width, height)
    output = np.empty((height, width, 3), dtype=np.uint8)
    threshold=0.50 #how strict the camera should recognize
    #writeLastModified(lines_to_write)# write the list of read id
    
    #---------------tagging the images--------------------
    file_enc=tag(threshold)
    #Initialize some variables
    face_locations = []
    face_encodings = []
    
    if app!=None:
        app.newPerson.put("#Start capturing...")
    while True:
        print("Capturing ...")
        if app!=None:
            if app.exitQueue.qsize()>0:
                if app.exitQueue.get()=='x':
                    #deleteFlickr()
                    break
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        print("Found {} face(s)".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)
        nameList=[]#list of file that matches
        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            name = "<Unknown Person>"
            for filename in file_enc :
                file_encodings=file_enc[filename]
                match = face_recognition.compare_faces(file_encodings, face_encoding,threshold)
                for m in match:
                    if m:
                        nameList.append(filename)
                        break
            print("{} detected!".format("Face"))
        if len(nameList)>0:
            if app!=None:
                print(nameList)
                app.newPerson.put(nameList)
                print(app.newPerson.qsize())
    
    camera.close()
    print("Stop capturing")

    #return known_encodings


def test(s):
    print(s)
if __name__ =="__main__":
    #p=RecognizeScript(camera=picamera.PiCamera())
    #p=Process(target=run_face_rec, args=(None,))
    #p.start()
    #p.join()
    tag()
    #with open("tag","rb") as f:
    #    print(pickle.load(f))
    #run_face_rec(None)
   
