import datetime
import time
import matplotlib.pyplot as pt
import sqlite3
from engine.command import speak
import os
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



def focus_graph():
    file = open("fgraph.txt", "r")
    cont = file.read()
    file.close()
    cont = cont.split(",")
    x1 = []

    for j in range(0, len(cont)):
        cont[j] = float(cont[j]) 
        x1.append(j)

    print(cont)
    y1 = cont

    pt.plot(x1, y1, color="red", marker="o")
    pt.title("YOUR FOCUS TIME", fontsize=16)
    pt.xlabel("Times", fontsize=14)
    pt.ylabel("Focus Time", fontsize=14)
    pt.grid()
    pt.show()
  
def focus_mode(st2):

  try:
    if not is_admin():
    # Re-run the script with administrator privileges
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    st1 = datetime.datetime.now().strftime("%H:%M")
    # st2 = custom_gui_input("Enter the Time eg:- [10:10] :- ")
    x = st1.replace(":", ".")
    if st2 == None:
        speak("Unable to enter in the focus mode")
        return
    y = st2.replace(":", ".")
    x = float(x)
    y = float(y)
    z = y - x
    z = round(z, 3)
    z = str(z)
    current_time=st1
    stop_time=st2
    host_path = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    redirect = "127.0.0.1"
    speak(f"Entering focus mode for Next {z} minutes")
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    query = "SELECT url FROM web_command IF category IN 'social media' "
    cursor.execute(query)
    website_list = cursor.fetchall()
    if current_time < stop_time:
        with open(host_path, "r+") as file:
            content = file.read()
            print("Processing...")

            # Write the blocking rules only if not already present
            to_write = [f"{redirect} {website}\n" for website in website_list if website not in content]
            if to_write:
                file.write(''.join(to_write))
                print("Websites blocked.")
                speak("Websites blocked.")
                speak("FOCUS MODE TURNED ON!!!")
            else:
                print("Websites already blocked.")
        
        # Monitoring focus time and turning off blocking after the stop time
        while datetime.datetime.now().strftime("%H:%M") < stop_time:
            time.sleep(60)  # Check every minute

        # Removing the blocked websites after the focus mode ends
        with open(host_path, "r+") as file:
            lines = file.readlines()
            file.seek(0)
            file.writelines([line for line in lines if not any(website in line for website in website_list)])
            file.truncate()
            print("FOCUS MODE IS OFF!!!")
            speak("FOCUS MODE IS OFF!!!")
    with open("engine\\fgraph.txt", "a") as file:
        file.write(f", {z}")
  except:
       print("Cannot Enter focus mode Something Went Wrong") 
    