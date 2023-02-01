#pip install opencv-python
#pip install SpeechRecognition
#pip install pyaudio (more complicated steps for mac and linux)
#pip install pyttsx3
import cv2 as cv2
import os
import numpy as numpy 
import pyttsx3
import threading
import json
import sys
import speech_recognition as sr


print(cv2.__version__)

engine = pyttsx3.init()

#used to store the quadrant the face is detected in
#global so that we can share it between sound and video thread
global quadrant
quadrant = "none"
#used to kill all threads from one thread
global killAllThreads
killAllThreads = False
#used to send photo command to video thread
global takePhoto
takePhoto = False

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

#load custom config file for houndify speach reconition
f = open("myConfig.json")
myConfig = json.load(f)

#setup speech recognition classes
r = sr.Recognizer()
mic = sr.Microphone()

#used to listen for sound input from mic
def listen_mic():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    return audio

#used to transcribe sound input into text
def transcribe_audio(audio):
    old_stdout = sys.stdout # backup current stdout
    sys.stdout = open(os.devnull, "w")
    #transcript = r.recognize_houndify(audio, myConfig["houndify"][0]["id"], myConfig["houndify"][0]["key"])
    transcript = r.recognize_houndify(audio, myConfig["houndify"][1]["id"], myConfig["houndify"][1]["key"])
    #transcript = r.recognize_houndify(audio, myConfig["houndify"][2]["id"], myConfig["houndify"][2]["key"])
    sys.stdout = old_stdout # reset old stdout
    if transcript[0] == "":
        return "Error"
    return transcript

#program introduction and instructions
engine.say("Welcome to the photo booth. Select which quadrant you'd like your face to be in from the following options: Top Left, Top Right, Bottom Left, Bottom Right.")
engine.runAndWait()

#get user quadrant from user using voice
user_quadrant = "none"
while user_quadrant == "none":
    audio = listen_mic()
    transcript = transcribe_audio(audio)
    if transcript[0] == "top left" or transcript[0] == "top right" or transcript[0] == "bottom right" or transcript[0] == "bottom left":
        user_quadrant = transcript[0]
    if transcript[0] == "done" or transcript[0] == "close program" or transcript[0] == "close":
        user_quadrant = "exit"
        killAllThreads = True

#more instructions
if killAllThreads == False:
    engine.say("The program will guide you by telling you which quadrant your face is in if you would like to take a picture in that quadrant say cheeese or press p.You may take a picture in a quadrant differnt from the one specified above. If the program says none than it can't detect your face, try to face the camera about an arms length away. To close the program say close program, done, or press q")
    engine.runAndWait() 

#sound output thread
def soundOutputLoop():
    global quadrant
    global killAllThreads
    localQuadrant = "none"
    while killAllThreads == False:
        if(localQuadrant != quadrant):
            localQuadrant = quadrant
            print(quadrant)
            engine.say(quadrant)
            engine.runAndWait()

#sound input thread
def soundInputLoop(user_quadrant):
    global quadrant
    global killAllThreads
    global takePhoto
    while killAllThreads == False:
        audio = listen_mic()
        transcript = transcribe_audio(audio)
        if(transcript[0] == "cheese" and quadrant == user_quadrant):
            takePhoto = True
            engine.say("photo taken")
            engine.runAndWait()
        elif(transcript[0] == "done" or transcript[0] == "close program" or transcript[0] == "close"):
             engine.say("Bye Bye for now!")
             engine.runAndWait()
             killAllThreads = True
        else:
            print(transcript[0])

#handle cv2 video and face reconition
def videoLoop(face_cascade, img_counter):
    global quadrant
    global killAllThreads
    global takePhoto
    #this captures video from laptop camera
    cap = cv2.VideoCapture(0) 

    #video thread on main thread
    while True:
        new_quadrant = "none" #default is none till we find a face

        ret,frame = cap.read() # reads the video input one frame at a time
        frame = cv2.flip(frame, 1)# horizontal flip to make sure that right and left is correct
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
        if key == ord("q") or killAllThreads == True: # press q to exit this while loop
             engine.say("Bye Bye for now!")
             engine.runAndWait()
             killAllThreads = True
             break
        if key == ord("p") or takePhoto == True:
            takePhoto = False
            img_name = "pictures/opencvframe{}.jpg".format(img_counter) #saves taken photo
            cv2.imwrite(img_name, frameCopy) 
            print("Photo Taken")
            img_counter+=1
    
    cap.release() #release video capture object
    cv2.destroyAllWindows() # Closes all frame windows

#handle threading for sound input and output
sithread = threading.Thread(target=soundOutputLoop)
sothread = threading.Thread(target=soundInputLoop, args=[user_quadrant])

sithread.start()
sothread.start()

#run video loop on main thread
videoLoop(face_cascade, img_counter)

sithread.join()
sothread.join()
