import csv
import sqlite3
import os
import win32com.client
import csv
import sqlite3

def get_start_menu_shortcuts(start_menu_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcuts = []
    
    # Walk through all files in the start menu directory
    for root, dirs, files in os.walk(start_menu_path):
        for file in files:
            if file.endswith(".lnk"):  # Check for shortcut files
                shortcut_path = os.path.join(root, file)
                shortcut = shell.CreateShortcut(shortcut_path)
                target_path = shortcut.TargetPath  # Get the target path
                shortcuts.append((file, target_path))
    
    return shortcuts

def addWindowsApp(con,cursor):
    # Start menu paths
    start_menu_user = os.path.join(os.environ['APPDATA'], r"Microsoft\\Windows\\Start Menu\\Programs")
    start_menu_all_users = os.path.join(os.environ['PROGRAMDATA'], r"Microsoft\\Windows\\Start Menu\\Programs")

    # Get shortcuts from both user and all-users start menu
    shortcuts = get_start_menu_shortcuts(start_menu_user) + get_start_menu_shortcuts(start_menu_all_users)
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()

    # Print the array of tuples (shortcut name, target path)
    for shortcut, target in shortcuts:
        shortcut = shortcut.replace(".lnk","")
        shortcut=shortcut.lower()
        print(f"{shortcut} -> {target}")
        query = "INSERT INTO sys_command VALUES (null,?, ?)"
        cursor.execute(query,(shortcut,target))
    con.commit()

def addWebsite(con,cursor):
    data = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "Bing", "url": "https://www.bing.com"},
    {"name": "Yahoo", "url": "https://www.yahoo.com"},
    {"name": "Facebook", "url": "https://www.facebook.com"},
    {"name": "Instagram", "url": "https://www.instagram.com"},
    {"name": "Twitter", "url": "https://www.twitter.com"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com"},
    {"name": "YouTube", "url": "https://www.youtube.com"},
    {"name": "Netflix", "url": "https://www.netflix.com"},
    {"name": "Vimeo", "url": "https://www.vimeo.com"},
    {"name": "Amazon", "url": "https://www.amazon.com"},
    {"name": "eBay", "url": "https://www.ebay.com"},
    {"name": "Alibaba", "url": "https://www.alibaba.com"},
    {"name": "BBC", "url": "https://www.bbc.com"},
    {"name": "CNN", "url": "https://www.cnn.com"},
    {"name": "The New York Times", "url": "https://www.nytimes.com"},
    {"name": "Wikipedia", "url": "https://www.wikipedia.org"},
    {"name": "Coursera", "url": "https://www.coursera.org"},
    {"name": "Khan Academy", "url": "https://www.khanacademy.org"},
    {"name": "Google Drive", "url": "https://www.drive.google.com"},
    {"name": "Dropbox", "url": "https://www.dropbox.com"},
    {"name": "OneDrive", "url": "https://www.onedrive.com"},
    {"name": "Reddit", "url": "https://www.reddit.com"},
    {"name": "Twitch", "url": "https://www.twitch.tv"},
    {"name": "Discord", "url": "https://www.discord.com"},
    {"name": "Slack", "url": "https://www.slack.com"},
    {"name": "Microsoft Teams", "url": "https://www.teams.microsoft.com"},
    {"name": "Zoom", "url": "https://www.zoom.us"},
    {"name": "Zara", "url": "https://www.zara.com"},
    {"name": "H&M", "url": "https://www.hm.com"},
    {"name": "ASOS", "url": "https://www.asos.com"}
    ]

# Using parameterized queries to prevent SQL injection
    for obj in data:
        query = "INSERT INTO web_command (name, url) VALUES (?, ?)"
        cursor.execute(query, (obj["name"].lower(), obj["url"]))
    con.commit()

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
addWindowsApp(con,cursor)

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
cursor.execute(query)
addWebsite(con,cursor)

# testing module
# app_name = "android studio"
# cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
# results = cursor.fetchall()
# print(results[0][0])

# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
# desired_columns_indices = [0, 30]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
con.close()

# query = "INSERT INTO contacts VALUES (null,'abhinav', '9810422278', 'null')"
# cursor.execute(query)
# con.commit()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])