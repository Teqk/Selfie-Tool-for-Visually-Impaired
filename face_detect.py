from cmath import rect
from curses.textpad import rectangle
from tkinter import image_names
from tkinter.tix import ButtonBox
import cv2 as cv
import os
import numpy as numpy 

cap = cv.VideoCapture(0)  #this captures video from laptop camera

img_counter = 0 
location = (0,0)
bottom_left =(10,10)
top_left =(20,80)
bottom_right = (80,20)
top_right = (80,80)
center = (50,50)

while cap.isOpened():
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
        hair_face_cascade = cv.CascadeClassifier("haarcascade_frontalface_default.xml")
        face = hair_face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors =5)
        for x,y,w,h in face:
            cv.rectangle(photo, (x,y), (x+w, y+h), (255,0,0), 5)
            cv.imshow("Face Detected", photo)
            #t")

            #if cv.rectangle(photo, (x,y), (x+w, y+h), (255,0,0), 5) ==
        print("Faces Found", len(face))

        #Next set center, left, right as certain pixels and create test to see if the face is there


cap.release() #release video capture object
cv.destroyAllWindows() # Closes all frame windowss

#Gains access to webcam