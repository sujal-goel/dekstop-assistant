import sqlite3
import eel

def createConnection():
    conn = sqlite3.connect('jarvis.db')
    cursor = conn.cursor()
    return conn, cursor

@eel.expose
def createContact(contact):
    try:
        conn, cursor = createConnection()
        cursor.execute("INSERT INTO contacts (name, email, mobile_no) VALUES (?, ?, ?)", 
                       (contact['name'], contact['email'], contact['phone']))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def readContacts():
    try:
        conn, cursor = createConnection()
        cursor.execute("SELECT * FROM contacts")
        contacts = cursor.fetchall()
        conn.close()
        return {"success": True, "contacts": contacts}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def updateContacts(contacts):
    try:
        conn, cursor = createConnection()
        for contact in contacts:
            cursor.execute("UPDATE contacts SET name = ?, email = ?, mobile_no = ? WHERE id = ?", 
                           (contact['name'], contact['email'], contact['phone'], contact['id']))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def deleteContact(contact_id):
    try:
        conn, cursor = createConnection()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@eel.expose
def fetch_contact_details():
    try:
        conn,cursor = createConnection()
        cursor.execute("SELECT name, email, mobile_no FROM contacts")
        contacts = cursor.fetchall()
        conn.close()

        # Convert each entry into an object and return an object of objects
        contact_dict = {}
        for contact in contacts:
            name, email, phone = contact
            contact_dict[name] = {
                "name": name,
                "email": email,
                "phone": phone
            }
        return contact_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}