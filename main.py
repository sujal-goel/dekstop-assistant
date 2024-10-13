import os
import eel
import json
from engine.features import *
from engine.command import *
from engine.login import getLogin
from engine.auth import recoganize


def start():
        eel.init("www")
        # user = User()
        # data = user.getLogin()
        @eel.expose
        def init():
          data = getLogin()
          playAssistantSound()
          if data!={}:
            subprocess.call([r'device.bat'])
            eel.hideLoader("FaceAuth")
            speak("Ready for Face Authentication")
            flag = recoganize.AuthenticateFace(data["userid"],data["name"])
            if flag == 1:
                eel.hideFaceAuth()
                speak("Face Authentication Successful")
                eel.hideFaceAuthSuccess()
                speak("Hello, Welcome Sir, How can i Help You")
                eel.hideStart()
                playAssistantSound()
            else:
                speak("Face Authentication Fail")
          else:  
              eel.hideLoader("login-form")
              speak("Login To Access")
              
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')

        eel.start('index.html', mode=None, host='localhost', block=True)
