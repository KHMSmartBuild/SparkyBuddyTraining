import re
import sqlite3

# Connect to the database
conn = sqlite3.connect('BS7671_database.db')
c = conn.cursor()

# Open the BS7671 standard file for parsing
with open('BS7671.txt', 'r') as f:
    current_chapter = ''
    current_section = ''
    current_paragraph = ''
    for line in f:
        # Check if the line contains a chapter title
        match = re.match(r'^\d{1,2}\s+[A-Z]', line)
        if match:
            # Extract the chapter title
            chapter_title = line.strip()
            # Add the chapter to the database
            c.execute("INSERT INTO Chapters (chapter_title) VALUES (?)", (chapter_title,))
            current_chapter = chapter_title
        # Check if the line contains a section title
        match = re.match(r'^\d{1,2}\.\d{1,2}\s+[A-Z]', line)
        if match:
            # Extract the section title
            section_title = line.strip()
            # Add the section to the database
            c.execute("INSERT INTO Sections (section_title, chapter_id) VALUES (?, (SELECT chapter_id FROM Chapters WHERE chapter_title=?))", (section_title, current_chapter))
            current_section = section_title
        # Check if the line contains a paragraph
        match = re.match(r'^\d{1,2}\.\d{1,2}\.\d{1,2}\s', line)
        if match:
            # Extract the paragraph text
            paragraph_text = line.strip()
            # Add the paragraph to the database
            c.execute("INSERT INTO Paragraphs (paragraph_text, section_id) VALUES (?, (SELECT section_id FROM Sections WHERE section_title=?))", (paragraph_text, current_section))

# Commit the changes and close the connection
conn.commit()
conn.close()