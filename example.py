#pip install SpeechRecognition
#pip install pyaudio (more complicated steps for mac and linux)
#pip install playsound
import speech_recognition as sr
from playsound import playsound #used to play sound back to the user
import sys
import os
import json

#load custom config file 
f = open("myConfig.json")
myConfig = json.load(f)

#setup speech recognition classes
r = sr.Recognizer()
mic = sr.Microphone()

def listen_mic():
    with mic as source:
        r.adjust_for_ambient_noise(source)
        playsound("beep-07.wav")
        audio = r.listen(source)
        playsound("beep-02.wav")
    return audio

def transcribe_audio(audio):
    old_stdout = sys.stdout # backup current stdout
    sys.stdout = open(os.devnull, "w")
    #transcript = r.recognize_houndify(audio, myConfig["houndify"][0]["id"], myConfig["houndify"][0]["key"])
    transcript = r.recognize_houndify(audio, myConfig["houndify"][1]["id"], myConfig["houndify"][1]["key"])
    #transcript = r.recognize_houndify(audio, myConfig["houndify"][2]["id"], myConfig["houndify"][2]["key"])
    sys.stdout = old_stdout # reset old stdout
    if transcript[0] == "":
        playsound("beep-03.wav")
        return "Error"
    return transcript

stop = False
while not stop:
    audio = listen_mic()
    transcript = transcribe_audio(audio)
    print(transcript)
    if transcript[0] == "exit" or transcript[0] == "done":
        stop = True