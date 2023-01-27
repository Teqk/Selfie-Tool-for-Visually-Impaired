from cmath import rect
from curses.textpad import rectangle
from tkinter import image_names
from tkinter.tix import ButtonBox
import cv2 as cv
import os
import numpy as numpy 
import time

cap = cv.VideoCapture(0)  #this captures video from laptop camera

img_counter = 0 

quadrant = "none"

while cap.isOpened():
    new_quadrant = "none"
    ret,frame = cap.read() # reads the image one by one
    if not ret:
        print("Unable to take picture")
        break

    cv.imshow("Your Perfect Selfie", frame) # displays a frame

    # EXITING 
    key =cv.waitKey(1) #wait until this key is pressed
    if key == ord("q"): # press q to exit this while loop
        break
    #Taking the Photo
    elif key == ord("p"): #key that takes a photo
        img_name = "opencvframe{}.jpg".format(img_counter) #saves taken photo
        cv.imwrite(img_name,frame) 
        print("Photo Taken")
        img_counter+=1

        #MAKING THE PHOTO GRAYSCALE
        photo = cv.imread(img_name)
        gray = cv.cvtColor(photo ,cv.COLOR_BGR2GRAY)
        #cv.imshow("Gray", gray)
       #Face Dectection

        frameCopy = frame # unaltered copy of the frame
        fheight , fwidth , fcolors = frame.shape #get frame width and height

        hair_face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        face = hair_face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors =5)
        for x,y,w,h in face:
            cv.rectangle(photo, (x,y), (x+w, y+h), (255,0,0), 5)
            #gets the x and y coordinates of the users face
            xper = int(((x+w/2)/fwidth)*100)
            yper = int(((y+h/2)/fheight)*100)
            #Defines positons for coordinates
            if xper < 50 and yper < 50:
                new_quadrant = "topleft"
            if xper >= 50 and yper < 50:
                new_quadrant = "topright"
            if xper < 50 and yper >= 50:
                new_quadrant = "bottomleft"
            if xper >= 50 and yper >= 50:
                new_quadrant = "bottomright"
    
        #update the quadrant when it changes
        if len(face) <= 1:
            if(new_quadrant != quadrant):
                quadrant = new_quadrant
                print(quadrant)

            #Shows picture taken
            cv.imshow("Face Detected", photo)
           
        print("Faces Found", len(face))

cap.release() #release video capture object
cv.destroyAllWindows() # Closes all frame windowss

