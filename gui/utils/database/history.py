# Script name : history.py
# Location = gui\utils\database\history.py
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
# Purpose:


import os
import sqlite3
from sqlite3 import Error

def check_if_table_exists(conn, table_name):
    """
    Check if a table exists in the database.
    """
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cur.fetchone() is not None

def create_connection(db_file):
    """Create a connection to a SQLite database."""
    conn = None
    try:
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_conversation_history_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        timestamp DATETIME NOT NULL
    );'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def insert_conversation_log(conn, log):
    """
    Insert a new conversation log into the conversation_history table.
    """
    sql = '''INSERT INTO conversation_history(user_input, ai_response, timestamp)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, log)
    conn.commit()
    return cur.lastrowid

def get_conversation_history(conn, limit=None):
    """
    Retrieve conversation logs from the conversation_history table.
    """
    cur = conn.cursor()
    if limit is None:
        cur.execute("SELECT * FROM conversation_history ORDER BY timestamp DESC")
    else:
        cur.execute("SELECT * FROM conversation_history ORDER BY timestamp DESC LIMIT ?", (limit,))

    return cur.fetchall()

def load_conversation_history(conn):
    """
    Retrieve conversation logs from the conversation_history table.
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM conversation_history ORDER BY timestamp DESC")

    return cur.fetchall()
def save_conversation_history(conn, history):
    """
    Insert a new conversation log into the conversation_history table.
    """
    sql = '''INSERT INTO conversation_history(user_input, ai_response, timestamp)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.executemany(sql, history)
    conn.commit()

def save_conversation_log(conn, log):
    """
    Insert a new conversation log into the conversation_history table.
    """
    sql = '''INSERT INTO conversation_history(user_input, ai_response, timestamp)
             VALUES(?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, log)
    conn.commit()

def delete_conversation_log(conn, log_id):
    """
    Delete a conversation log from the conversation_history table.
    """
    sql = '''DELETE FROM conversation_history WHERE id=?'''
    cur = conn.cursor()
    cur.execute(sql, (log_id,))
    conn.commit()

def delete_all_conversation_logs(conn):
    """
    Delete all conversation logs from the conversation_history table.
    """
    sql = '''DELETE FROM conversation_history'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases/conversation_history.db")
conn = create_connection(db_path)
if not check_if_table_exists(conn, 'conversation_history'):
    create_conversation_history_table(conn)
