# Script name : knowledge_base.py
#Location = gui\utils\prep\knowledge_base.py
# Author: KHM Smartbuild
# Purpose: 
"""
This script creates a SQLite database with a table called electrical_knowledge, 
which stores information about electrical systems

"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild


import logging
import sqlite3

DB_FILE = "knowledge_base.db"

def create_connection(database_file: str) -> sqlite3.Connection:
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(database_file)
    except sqlite3.Error as e:
        logging.error(e)
    return conn


def create_table(conn: sqlite3.Connection, create_table_sql: str) -> None:
    """Create a table from the create_table_sql statement."""
    try:
        with conn:
            conn.execute(create_table_sql)
    except sqlite3.Error as e:
        logging.error(e)


def main() -> None:

    # Create table SQL statement
    create_electrical_knowledge_table = """CREATE TABLE IF NOT EXISTS electrical_knowledge (
                                            id INTEGER PRIMARY KEY,
                                            category TEXT NOT NULL,
                                            subcategory TEXT,
                                            content TEXT NOT NULL,
                                            tags TEXT
                                        );"""

    # Create a database connection and table
    with create_connection(DB_FILE) as conn:
        if conn is not None:
            create_table(conn, create_electrical_knowledge_table)
        else:
            logging.error("Cannot create the database connection.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
