import sqlite3
from sqlite3 import Error

def create_connection(database_file):
    conn = None
    try:
        conn = sqlite3.connect(database_file)
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_electrical_knowledge(conn, electrical_knowledge):
    sql = '''INSERT INTO electrical_knowledge(category, subcategory, content, tags)
             VALUES(?,?,?,?)'''
    cur = conn.cursor()
    try:
        cur.execute(sql, electrical_knowledge)
        conn.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
        conn.rollback()

def get_electrical_knowledge_by_category(conn, category):
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM electrical_knowledge WHERE category=?", (category,))
        return cur.fetchall()
    except Error as e:
        print(e)
        conn.rollback()

def update_electrical_knowledge(conn, knowledge):
    sql = '''UPDATE electrical_knowledge
             SET category = ?,
                 subcategory = ?,
                 content = ?,
                 tags = ?
             WHERE id = ?'''
    cur = conn.cursor()
    try:
        cur.execute(sql, knowledge)
        conn.commit()
    except Error as e:
        print(e)
        conn.rollback()

def main():

    database_file = 'data.db'

    create_electrical_knowledge_table = '''CREATE TABLE IF NOT EXISTS electrical_knowledge (
                                        id integer PRIMARY KEY,
                                        category text NOT NULL,
                                        subcategory text NOT NULL,
                                        content text,
                                        tags text NOT NULL
                                    );'''

    conn = create_connection(database_file)
    if conn is not None:
        create_table(conn, create_electrical_knowledge_table)

        knowledge_data = ('Wiring and Circuit Design', 'Circuit diagrams and symbols', 'Sample content', 'circuit_diagrams, symbols')
        knowledge_id = insert_electrical_knowledge(conn, knowledge_data)
        print(f"Inserted record with ID: {knowledge_id}")

        category = 'Wiring and Circuit Design'
        knowledge_records = get_electrical_knowledge_by_category(conn, category)
        for record in knowledge_records:
            print(record)

        updated_knowledge_data = ('Updated Category', 'Updated Subcategory', 'Updated Content', 'updated_tags', knowledge_id)
        update_electrical_knowledge(conn, updated_knowledge_data)

    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    main()
