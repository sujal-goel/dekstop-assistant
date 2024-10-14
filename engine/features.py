import os
from pipes import quote
import re
import sqlite3
import struct
import datetime
import subprocess
import time
import webbrowser
from playsound import playsound
import speedtest
import eel
import pyaudio
import pyautogui
import googletrans
import requests
import wikipedia
from bs4 import BeautifulSoup

from gtts import gTTS
from pynput.keyboard import Key, Controller
from engine.command import speak,takecommand
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    if ASSISTANT_NAME in query:
        query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except (IndexError, FileNotFoundError, sqlite3.Error) as e:
            speak(f"some thing went wrong ")
            print(e)

       
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()




# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

# youtube automation
def pausenplay():
    pyautogui.press('k')

def muteUnMute():
    keyboard = Controller()
    keyboard.press(Key.media_volume_mute)
    keyboard.release(Key.media_volume_mute)

def volumeDown():
    keyboard = Controller()
    for i in range(5):
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        time.sleep(0.1)
    speak("VOLUME IN DECREASED")   

def volumeUp():
    keyboard = Controller()
    for i in range(5):
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        time.sleep(0.1)
    speak("VOLUME IS INCREASED")   

# Handle translation
def translate_text(query):
    speak("SURE SIR")
    query = query.replace("translate", "").strip()
    if "in" in query:
        query_split = query.split("in")
    elif "to" in query:
        query_split = query.split("to")
    else:
        speak("Sorry, I didn't understand the language to translate to.")
        return
    
    text_to_translate = query_split[0].strip()
    target_language_name = query_split[1].strip()
    translator = googletrans.Translator()
    dest_language = None
    for key, value in googletrans.LANGUAGES.items():
        if value == target_language_name:
            dest_language = key
            break
    if dest_language is None:
        speak(f"Sorry, I couldn't find the language '{target_language_name}'.")
        return
    
    translation = translator.translate(text_to_translate, dest=dest_language)
    text = translation.text
    text = "we say it as "+text
    print(text)
    speak(text)
    # speakg1 = gTTS(text=text, lang=dest_language, slow=False)
    # speakg1.save("voice.mp3")
    # playsound("voice.mp3")
    # os.remove("voice.mp3")  

def whattime():
    curr_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {curr_time}")     

def temp(city):
     
     url = f"https://www.google.com/search?q=temperature+in+{city}"
     r = requests.get(url)
     soup = BeautifulSoup(r.text, 'html.parser')
     temp = soup.find('div', class_="BNeawe").text
     speak(f"The current temperature in {city} is {temp}")

def int_speed():
    try:
        st = speedtest.Speedtest()

        st.get_best_server()

        download_speed = st.download() / 1_000_000  
        upload_speed = st.upload() / 1_000_000      

        speak(f"Upload speed is {upload_speed:.2f} Mbps and download speed is {download_speed:.2f} Mbps")
    except Exception as e:
        speak(f"An error occurred while testing internet speed: {e}")
        
def wikiSearch():
    speak('Searching Wikipedia...')
    query = query.replace("wikipedia", "")
    results = wikipedia.summary(query, sentences=2) 
    speak(results)
# print all the languages
# print(googletrans.LANGUAGES)