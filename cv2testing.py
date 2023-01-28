#pip install opencv-python
import cv2 as cv2
import os
import numpy as numpy 
import pyttsx3
import threading

print(cv2.__version__)

engine = pyttsx3.init()

#used to store the quadrant the face is detected in
#global so that we can share it between sound and video thread
global quadrant
quadrant = "none"
#used to kill the sound thread from the video thread
global killAllThreads
killAllThreads = False

#determine the starting point for the image counter 
#based on current files in the pictures folder
def starts_with(string):
    if string.startswith("opencvframe"):
        return True
    else:
        return False

img_counter = len(list(filter(starts_with,os.listdir("pictures"))))

#face classifier data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#TODO: ### interaction with client welcome them to aplication
#ask them if they want to be in top left etc...
#error checking for bad input...

#this captures video from laptop camera
cap = cv2.VideoCapture(0)  

#video thread
def videoLoop(face_cascade, img_counter):
    global quadrant
    global killAllThreads
    while True:
        new_quadrant = "none" #default is none till we find a face

        ret,frame = cap.read() # reads the video input one frame at a time
        frameCopy = frame # unaltered copy of the frame
        fheight , fwidth , fcolors = frame.shape #get frame width and height

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts frame to greyscale
        faces = face_cascade.detectMultiScale(gray, 1.1, 6) #detects faces on frame
        for (x, y, w, h) in faces: 
            #draw a rectangle around faces
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
            #detect what quadrant the face is in
            xper = int(((x+w/2)/fwidth)*100)
            yper = int(((y+h/2)/fheight)*100)
            
            if xper < 50 and yper < 50:
                new_quadrant = "top left"
            if xper >= 50 and yper < 50:
                new_quadrant = "top right"
            if xper < 50 and yper >= 50:
                new_quadrant = "bottom left"
            if xper >= 50 and yper >= 50:
                new_quadrant = "bottom right"
        
        #update the quadrant when it changes
        if len(faces) <= 1:
            if(new_quadrant != quadrant):
                quadrant = new_quadrant
        
        cv2.imshow("Picture", frame) #displays a frame

        key = cv2.waitKey(1) #wait until this key is pressed
        if key == ord("q"): # press q to exit this while loop
            killAllThreads = True
            break
        if key == ord("p"):

            # TODO: ### if user in correct quadrant and cheese voice command 
            
            img_name = "pictures/opencvframe{}.jpg".format(img_counter) #saves taken photo
            cv2.imwrite(img_name, frameCopy) 
            print("Photo Taken")
            img_counter+=1

#sound thread
def soundLoop():
    global quadrant
    global killAllThreads
    localQuadrant = "none"
    while killAllThreads == False:
        if(localQuadrant != quadrant):
            localQuadrant = quadrant
            print(quadrant)
            engine.say(quadrant)
            engine.runAndWait()

#handle threading
vthread = threading.Thread(target=videoLoop, args=[face_cascade, img_counter])
sthread = threading.Thread(target=soundLoop)

vthread.start()
sthread.start()

vthread.join()
sthread.join()

cap.release() #release video capture object
cv2.destroyAllWindows() # Closes all frame windows
