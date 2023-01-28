import cv2
import os
import pyttsx3
import numpy as np

engine = pyttsx3.init()

print(cv2.__version__)

#determine the starting point for the image counter
#based on current files in the pictures folder
def starts_with(string):
    if string.startswith("opencvframe"):
        return True
    else:
        return False

img_counter = len(list(filter(starts_with,os.listdir("pictures"))))


#used to store the quadrant the face is detected in
quadrant = "none"

#face classifier data
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#TODO: ### interaction with client welcome them to aplication
#ask them if they want to be in top left etc...
#error checking for bad input...

#this captures video from laptop camera
cap = cv2.VideoCapture(0)

# edit here for more Introduction
engine.say("Welcome to the photo booth. Please move your head to the quadrant where you want your photo to be taken.")
engine.runAndWait()

while True:
    new_quadrant = "none" #default is none till we find a face

    ret,frame = cap.read() # reads the video input one frame at a time
    frameCopy = frame # unaltered copy of the frame
    fheight , fwidth , fcolors = frame.shape #get frame width and height

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #converts frame to greyscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 4) #detects faces on frame
    for (x, y, w, h) in faces:
        #draw a rectangle around faces
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        #detect what quadrant the face is in
        xper = int(((x+w/2)/fwidth)*100)
        yper = int(((y+h/2)/fheight)*100)
        
        if xper < 50 and yper < 50:
            new_quadrant = "topleft"
        if xper >= 50 and yper < 50:
            new_quadrant = "topright"
        if xper < 50 and yper >= 50:
            new_quadrant = "bottomleft"
        if xper >= 50 and yper >= 50:
            new_quadrant = "bottomright"
    
    #update the quadrant when it changes
    if len(faces) <= 1:
        if(new_quadrant != quadrant):
            quadrant = new_quadrant
            print(quadrant)
            if quadrant == "topleft":
                engine.say("You are in the top left corner.")
                engine.runAndWait()
            elif quadrant == "topright":
                engine.say("You are in the top right corner.")
                engine.runAnd
            elif quadrant == "bottomleft":
                engine.say("Move your head to the bottom left corner")
                engine.runAndWait()
            elif quadrant == "bottomright":
                engine.say("Move your head to the bottom right corner")
                engine.runAndWait()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
