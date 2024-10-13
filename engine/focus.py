# import ctypes
# import sys
import datetime
import time
import matplotlib.pyplot as pt
from engine.command import speak,takecommand
import sqlite3

def createConnection():
    con = sqlite3.connect("./jarvis.db")
    cursor = con.cursor()
    query = "CREATE TABLE IF NOT EXISTS blockedSites(name VARCHAR,url VARCHAR)"
    cursor.execute(query)
    return con,cursor

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


def is_admin(st1, st2):
    # try:
    #     return ctypes.windll.shell32.IsUserAnAdmin()
    # except:
    #     return False

    current_time = st1
    Stop_time = st2

    host_path = "C:\Windows\System32\drivers\etc\hosts"
    redirect = "127.0.0.1"
    print(f"current time is:- {current_time}")
    time.sleep(2)
    con,cursor = createConnection()
    query="Select url from blockedSites"
    cursor.execute(query)
    website_list =  cursor.fetchall()
    if current_time < Stop_time:
        with open(host_path, "r+") as file:
            content = file.read()
            time.sleep(2)
            print("processing.....!!")
            for website in website_list:
                if website in content:
                    pass
                else:
                    file.write(f"{redirect} {website}\n")
                    time.sleep(1)
            print("FOCUS MODE TURN ON!!!")

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_time = float(current_time.replace(":","."))
        if current_time >= Stop_time:
            with open(host_path, "r+") as file:
                content = file.readlines()
                file.seek(0)

                for line in content:
                    if not any(website in line for website in website_list):
                        file.write(line)
                file.truncate()
                print("FOCUS MODE IS OFF..!!!")
                break


# else:
#     ctypes.windll.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)


def res():
    st1 = datetime.datetime.now().strftime("%H:%M")
    speak("for how many minutes ")
    z = takecommand()
    if ("minutes" in z):
        z.replace("minutes","")
    z=int(z)
    hours = 0
    if z==0:
        return 
    else:
        hours = z/60
    st2 = float(st1.replace(":","."))+ hours
    with open("fgraph.txt", "a") as file:
        file.write(f", {str(hours)}")
        file.close()
    is_admin(st1, st2)
    speak("Do you want to create focus graph")
    z = takecommand().lower()
    if z == "yes":
        focus_graph()
    else:
        pass


res()
