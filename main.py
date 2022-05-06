from gtts import gTTS
import random
import time
import pyglet
import os
import speech_recognition as sr
from datetime import datetime
import requests

def listen_command():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            our_speech = r.recognize_google(audio, language="ru")
            print("Вы сказали: " + our_speech)
            return our_speech
        except sr.UnknownValueError:
            return "ошибка"
        except sr.RequestError:
            return "ошибка"
    #return input("Say something: ")

def do_command(message):
    message = message.lower()
    if ("неон" in message) or ("nion" in message) or ("nioh" in message):
        if ("пока" in message):
            say_message("Не смею вас задерживать")
            exit()  # выход из программы

        if "привет" in message:
                say_message("Привет, я голосовой помощник!")
        if ("время" in message) or ("времени" in message) or ("час" in message) or ("часов" in message):
                current_datetime = datetime.now()
                say_message(str(current_datetime.hour) + " Часов " + str(current_datetime.minute) + " минут")
        #else:
            #say_message("Я вас не понял")

def say_message(message):
    voice = gTTS(message, lang="ru")
    file_voice_name = "_audio_"+str(random.randint(0,100000))+".mp3"
    voice.save(file_voice_name)
    sound = pyglet.media.load(file_voice_name)
    sound.play()
    print("Голосовой ассистент: "+message)
    os.remove(file_voice_name)

def weather():
    s_city = "Petersburg,RU"
    city_id = 0
    appid = "буквенно-цифровой APPID"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass

    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
    except Exception as e:
        print("Exception (weather):", e)
        pass

if __name__ == '__main__':
    while True:
        command = listen_command()
        do_command(command)

