import sqlite3

# Create the database and connect to it
conn = sqlite3.connect('BS7671_database.db')

# Create the Chapters table
conn.execute('''
    CREATE TABLE Chapters (
        chapter_id INTEGER PRIMARY KEY,
        chapter_title TEXT
    )
''')

# Create the Sections table
conn.execute('''
    CREATE TABLE Sections (
        section_id INTEGER PRIMARY KEY,
        section_title TEXT,
        chapter_id INTEGER,
        FOREIGN KEY (chapter_id) REFERENCES Chapters(chapter_id)
    )
''')

# Create the Paragraphs table
conn.execute('''
    CREATE TABLE Paragraphs (
        paragraph_id INTEGER PRIMARY KEY,
        paragraph_text TEXT,
        section_id INTEGER,
        FOREIGN KEY (section_id) REFERENCES Sections(section_id)
    )
''')

# Create the Images table
conn.execute('''
    CREATE TABLE Images (
        image_id INTEGER PRIMARY KEY,
        image_path TEXT,
        paragraph_id INTEGER,
        FOREIGN KEY (paragraph_id) REFERENCES Paragraphs(paragraph_id)
    )
''')

# Create the Definitions table
conn.execute('''
    CREATE TABLE Definitions (
        definition_id INTEGER PRIMARY KEY,
        term TEXT,
        definition_text TEXT
    )
''')

# Create the Examples table
conn.execute('''
    CREATE TABLE Examples (
        example_id INTEGER PRIMARY KEY,
        example_text TEXT,
        paragraph_id INTEGER,
        FOREIGN KEY (paragraph_id) REFERENCES Paragraphs(paragraph_id)
    )
''')

# Create the Questions table
conn.execute('''
    CREATE TABLE Questions (
        question_id INTEGER PRIMARY KEY,
        question_text TEXT,
        section_id INTEGER,
        FOREIGN KEY (section_id) REFERENCES Sections(section_id)
    )
''')

# Create the Answers table
conn.execute('''
    CREATE TABLE Answers (
        answer_id INTEGER PRIMARY KEY,
        answer_text TEXT,
        question_id INTEGER,
        FOREIGN KEY (question_id) REFERENCES Questions(question_id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()