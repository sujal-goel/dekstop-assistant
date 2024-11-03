import sqlite3
import json
import cv2
import os
import uuid
import shutil # to delete complete dir
from engine.auth.trainer import *
# from auth.trainer import *
import eel

@eel.expose
def createConnection():
    con = sqlite3.connect("./jarvis.db")
    cursor = con.cursor()
    query = "CREATE TABLE IF NOT EXISTS user(userid TEXT primary key, name VARCHAR(100), email VARCHAR(1000),phone VARCHAR(10),password varchar(100))"
    cursor.execute(query)
    return con,cursor
@eel.expose
def createAuthenticateUser(name,email,phone,password,save):
      con,cursor = createConnection()
      userid = str(uuid.uuid4())
      output_dir=f"engine\\auth\\samples\\{userid}"
      num_images=200
      if not os.path.exists(output_dir):
          os.makedirs(output_dir)
      # Access the camera (0 is usually the default camera)
      cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
      cap.set(3,640)
      cap.set(4,400)
    #   detector = cv2.CascadeClassifier('engine\\auth\\haarcascade_frontalface_default.xml')
      # Check if camera opened successfully
      if not cap.isOpened():
         print("Error: Could not open the camera.")
         return False
      count = 0
      while count < num_images:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break
            # converted_image =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(frame, 1.3, 5)
            img_name = os.path.join(output_dir, f'face.1.{count+1}.jpg')
            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2) #used to draw a rectangle on any image
            # Save the image
                cv2.imwrite(img_name, frame[y:y+h,x:x+w])
                print(f"Captured {img_name}")
                count += 1
                cv2.imshow('image', frame)
         # Wait for 1ms and break if 'q' is pressed
                if cv2.waitKey(1) & 0xFF == ord('q'):
                 break
         # Release the camera and close windows
      cap.release()
      count =0
      cv2.destroyAllWindows()
      train(output_dir,userid)
      query = 'INSERT INTO user VALUES (?,?,?,?,?)'
      cursor.execute(query,(userid,name,email,phone,password))
      con.commit()
      if (save):
         with open("engine\\auth\\user.json","w") as jsonfile: 
          json.dump({"userid" : userid,"name" : name,"email" : email},jsonfile,indent=4)
      shutil.rmtree(output_dir)
      return True

@eel.expose
def login(email,password):
    con,cursor = createConnection()
    query = "SELECT userid,name,email FROM user WHERE email=? and password=?"
    cursor.execute(query,(email,password))
    data = cursor.fetchone()
    if data==None:
        return False
    else:
        with open("engine\\auth\\user.json","w") as jsonfile:
            json.dump({"userid":data[0],"name":data[1],"email":data[2]},jsonfile,indent=4)
        return True
@eel.expose
def isUserlogin():
    with open("engine\\auth\\user.json","r") as jsonfile:
        if(json.load(jsonfile)=={}):
            return False
        else:
            return True

@eel.expose                
def getLogin():
    with open("engine\\auth\\user.json","r") as jsonfile:
        return json.load(jsonfile)       
@eel.expose
def logout():
    with open("engine\\auth\\user.json","w") as jsonfile:
        json.dump({},jsonfile)
    eel.hideLoader("login-form")
    eel.DisplayMessage("Login to Access")

@eel.expose
def getUserDetails():
   try: 
    data = getLogin()
    conn,cursor = createConnection()
    cursor.execute("SELECT * FROM user WHERE userid = ?",(data["userid"],))  # Assuming user ID is 1
    user_details = cursor.fetchone()
    conn.close()
    if user_details:
        return {
            "userid": user_details[0],
            "username": user_details[1],
            "email": user_details[2],
            "phone": user_details[3],
            "password": user_details[4]
        }
    else:
        return {}
   except Exception as e:
       pass
@eel.expose
def updateUser(updated_details):

    try:
        data = getLogin()
        conn,cursor = createConnection()
    
        cursor.execute("""
            UPDATE user
            SET name = ?, email = ?, phone = ?, password = ?
            WHERE userid = ?
        """, (updated_details["username"], updated_details["email"], updated_details["phone"], updated_details["password"],data["userid"]))
        
        conn.commit()
        conn.close()

        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
