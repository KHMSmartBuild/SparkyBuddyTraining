# Script name : insert_conversation_log.py
# location = gui\Sparky\insert_conversation_log.py
# accessable from Libraries = yes
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
# Purpose:


import json
import sqlite3
from utils.database.history import insert_conversation_log, save_conversation_history

# Create a connection to the SQLite database (replace "your_database.db" with your database file name)
conn = sqlite3.connect("conversation_history.db")

# Read the JSON file
with open("gui/openai/convo-1.js", "r") as file:
    content = file.read()
    print(content)
    conversation_data = json.loads(content)

# Extract the conversation logs
conversation_logs = conversation_data["conversations"][0]

# Insert the logs into the database
for i, log in enumerate(conversation_logs):
    role = log["role"]
    content = log["content"]

    if role == "user":
        user_input = content
        if i > 0:
            timestamp = prev_timestamp
            insert_conversation_log(conn, (user_input, ai_response, timestamp))
    elif role == "sparky":
        ai_response = content
        prev_timestamp = log.get("timestamp", "2023-04-26T12:00:00Z")

# Close the connection
conn.close()
