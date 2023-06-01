# -*- coding: utf-8 -*-
"""
@author: Satyajit Pattnaik

"""

from flask import Flask,render_template,redirect,request
import warnings
warnings.filterwarnings('ignore')


import speech_recognition as sr
import pyttsx3
# import pywhatkit
import datetime
import pyjokes
import wikipedia
import sys
import requests, json 
import time
listener = sr.Recognizer()
#engine = pyttsx3.init()


import re
import spacy

# Load the English language model for NER
nlp = spacy.load('en_core_web_sm')

audio_data_speech = ""
# Function to extract programming language from text
def extract_programming_language(text):
    programming_languages = ['python', 'data','java', 'c++', 'javascript','dataanalysis','analysys']  # Add more programming languages as needed
    for language in programming_languages:
        if re.search(fr'\b{language}\b', text, re.IGNORECASE):
            return language
    return None

# Function to extract experience from text
def extract_experience(text):
    experience_keywords = ['experience', 'background', 'years']  # Add more experience-related keywords as needed
    experience = None
    doc = nlp(text)
    for entity in doc.ents:
        if entity.label_ == 'DATE' or any(keyword in entity.text.lower() for keyword in experience_keywords):
            experience = entity.text
            break
    return experience

import os

app = Flask("__name__")

def engine_talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

    
def user_commands():
    command = "play"
    try:
        with sr.Microphone() as source:
            print("Start Speaking!!")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            command = command.replace('alexa', '')
            if 'alexa' in command:
                print(command)
    except:
        pass
    return command

def weather(city):
    # Enter your API key here 
    api_key = "<YOUR API KEY>"
    #How to use api_key, see the below code:
    #api_key = "ABCDE"
    
    # base_url variable to store url 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Give city name 
    city_name = city
    
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json() 
    
    # Now x contains list of nested dictionaries 
    # Check the value of "cod" key is equal to 
    # "404", means city is found otherwise, 
    # city is not found 
    if x["cod"] != "404": 
    
        # store the value of "main" 
        # key in variable y 
        y = x["main"] 
    
        # store the value corresponding 
        # to the "temp" key of y 
        current_temperature = y["temp"] 
        temp_in_celcius = current_temperature - 273.15
        return str(int(temp_in_celcius))
    
    
def run_alexa(command_speech):
    # command = user_commands()
    command = str(command_speech)
    if 'Alexa' in command:
        engine_talk("Hey How are you Please tell me about your self.")
    elif 'play' in command:
        song = command.replace('play', '')
        engine_talk('Playing....' + song)
        print("Playing....")
        # pywhatkit.playonyt(song)     
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        engine_talk('Current Time is' + time)
    elif 'joke' in command:
        get_j = pyjokes.get_joke()
        print(get_j)
        engine_talk(get_j)
    elif 'stop' in command:
        engine_talk("Good bye")
    else:
        engine_talk("I didn't hear you properly")
        print("I didn't hear you properly")


@app.route('/')
def hello():
    return render_template("alexa.html")

@app.route("/home")
def home():
    return redirect('/')

@app.route('/',methods=['POST', 'GET'])
def submit():
    while True:
        run_alexa()
    return render_template("alexa.html")


    
# Function to ask Python interview questions
def ask_python_questions():
    engine_talk("Great! Let's proceed with Python interview questions.")
    print("Great! Let's proceed with Python interview questions.")
    global audio_data_speech
    
    # Add your Python interview questions here
    questions = [
        "What is the difference between a list and a tuple in Python?",
        "How do you handle exceptions in Python?",
        "What is the purpose of the 'self' keyword in Python?",
        # Add more questions as needed
    ]
    
    # Loop through the questions and ask the user
    for i, question in enumerate(questions, start=1):
        print(f"Question {i}: {question}")
        
        engine_talk(f"Question {i}: {question}")
        print("Please provide your answer.")
        engine_talk("Please provide your answer.")
        print("Audio Data Speech : 1",audio_data_speech)
        time.sleep(20)
        print("Audio Data Speech : 2",audio_data_speech)
        # Transcribe the user's answer from speech
        # audio_file = "user_answer.wav"  # Replace with the path to the audio file
        # user_answer = transcribe_audio(audio_file)
        
        # print("User's Answer:", user_answer)
        print("")

def ask_data_analysys_questions():
    engine_talk("Great! Let's proceed with Data Analysys interview questions.")
    
    
    # Add your Python interview questions here
    questions = [
        "What is data analytics?",
        "What is the difference between descriptive and predictive analytics?",
        "What is the purpose of data cleaning?",
        "What is the central limit theorem?",
        "What is the purpose of data visualization?",
        "How do you handle missing data in your analysis?"
        # Add more questions as needed
    ]
    
    # Loop through the questions and ask the user
    for i, question in enumerate(questions, start=1):
        print(f"Question {i}: {question}")
        
        engine_talk(f"Question {i}: {question}")
        print("Please provide your answer.")
        engine_talk("Please provide your answer.")
        time.sleep(3)
        # Transcribe the user's answer from speech
        # audio_file = "user_answer.wav"  # Replace with the path to the audio file
        # user_answer = transcribe_audio(audio_file)
        
        # print("User's Answer:", user_answer)
        print("")
@app.route('/speech', methods=['POST'])
def process_speech():
    global audio_data_speech
    audio_data = request.data  # Raw audio data sent from the client
    # Process the audio data as needed (e.g., save to a file, perform speech-to-text conversion)
    # You can also respond with any data back to the client if required
    audio_data_speech = str(request.data)
    print("Audio Data : ",audio_data)
    user_intro = "Hello, I'm John. I have been programming in Python for the past 5 years."
    programming_language = extract_programming_language(str(audio_data))
    experience = extract_experience(str(audio_data))
    if programming_language != None or experience != None:
        # engine_talk(experience)
        # engine_talk(programming_language)
        if programming_language == "python" or "python" in experience.lower():
            print("User has experience in Python.")

            ask_python_questions()
            print("User has experience in Python.",audio_data)
    run_alexa(audio_data)
    return 'Success'  # Send a response to the client


if __name__ =="__main__":
    app.run(debug=True)
