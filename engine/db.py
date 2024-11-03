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
    {"name": "Google", "url": "https://www.google.com", "category": "Search Engine"},
    {"name": "Bing", "url": "https://www.bing.com", "category": "Search Engine"},
    {"name": "Yahoo", "url": "https://www.yahoo.com", "category": "Search Engine"},
    {"name": "Facebook", "url": "https://www.facebook.com", "category": "Social Media"},
    {"name": "Instagram", "url": "https://www.instagram.com", "category": "Social Media"},
    {"name": "Twitter", "url": "https://www.twitter.com", "category": "Social Media"},
    {"name": "LinkedIn", "url": "https://www.linkedin.com", "category": "Social Media"},
    {"name": "YouTube", "url": "https://www.youtube.com", "category": "Video Streaming"},
    {"name": "Netflix", "url": "https://www.netflix.com", "category": "Video Streaming"},
    {"name": "Vimeo", "url": "https://www.vimeo.com", "category": "Video Streaming"},
    {"name": "Amazon", "url": "https://www.amazon.com", "category": "E-commerce"},
    {"name": "eBay", "url": "https://www.ebay.com", "category": "E-commerce"},
    {"name": "Alibaba", "url": "https://www.alibaba.com", "category": "E-commerce"},
    {"name": "BBC", "url": "https://www.bbc.com", "category": "News"},
    {"name": "CNN", "url": "https://www.cnn.com", "category": "News"},
    {"name": "The New York Times", "url": "https://www.nytimes.com", "category": "News"},
    {"name": "Wikipedia", "url": "https://www.wikipedia.org", "category": "Educational"},
    {"name": "Coursera", "url": "https://www.coursera.org", "category": "Educational"},
    {"name": "Khan Academy", "url": "https://www.khanacademy.org", "category": "Educational"},
    {"name": "Google Drive", "url": "https://www.drive.google.com", "category": "Cloud Storage"},
    {"name": "Dropbox", "url": "https://www.dropbox.com", "category": "Cloud Storage"},
    {"name": "OneDrive", "url": "https://www.onedrive.com", "category": "Cloud Storage"},
    {"name": "Reddit", "url": "https://www.reddit.com", "category": "Social Media"},
    {"name": "Twitch", "url": "https://www.twitch.tv", "category": "Video Streaming"},
    {"name": "Discord", "url": "https://www.discord.com", "category": "Social Media"},
    {"name": "Slack", "url": "https://www.slack.com", "category": "Communication"},
    {"name": "Microsoft Teams", "url": "https://www.teams.microsoft.com", "category": "Communication"},
    {"name": "Zoom", "url": "https://www.zoom.us", "category": "Communication"},
    {"name": "Zara", "url": "https://www.zara.com", "category": "E-commerce"},
    {"name": "H&M", "url": "https://www.hm.com", "category": "E-commerce"},
    {"name": "ASOS", "url": "https://www.asos.com", "category": "E-commerce"}
]


# Using parameterized queries to prevent SQL injection
    for obj in data:
        query = "INSERT INTO web_command (name, url,category) VALUES (?, ?, ?)"
        cursor.execute(query, (obj["name"].lower(), obj["url"],obj["category"].lower()))
    con.commit()

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()
query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)
addWindowsApp(con,cursor)

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000), category VARCHAR(50))"
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

query = "INSERT INTO contacts VALUES (null,'abhinav', '9810422278', 'null')"
cursor.execute(query)
# con.commit()
con.commit()
con.close()

# query = 'kunal'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])