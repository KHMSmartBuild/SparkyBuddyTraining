# Script name : insert_electrical_knowledge.py
#Location = gui\utils\prep\insert_electrical_knowledge.py
# Author: KHM Smartbuild
# Purpose: 
"""
This script inserts a new row of data into the electrical_knowledge table.

"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import sqlite3

def insert_data(conn, category, subcategory, content, tags):
    """
    Insert a new row of data into the electrical_knowledge table.
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO electrical_knowledge (category, subcategory, content, tags) VALUES (?, ?, ?, ?)", (category, subcategory, content, tags))
    conn.commit()

# Example usage
database_file = "knowledge_base.db"
conn = sqlite3.connect(database_file)
insert_data(conn, "wiring", "residential", "The maximum permitted earth fault loop impedance for a 20A circuit with a type C circuit breaker is 1.44 ohms, according to BS7671.", "earth fault loop impedance, 20A circuit, type C circuit breaker, BS7671")
conn.close()
