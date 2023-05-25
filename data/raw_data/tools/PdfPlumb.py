import os
import pdfplumber
import sqlite3
import re

# Define the directory to search
directory = r"C:\Users\User\OneDrive\Desktop\training\Electrician"

# Connect to the SQLite database
database_path = r"C:\Users\User\OneDrive\Desktop\Buisness\KHM Smart Build\Projects\Training data\Sparky  training\databases\knowledge_base.db"
conn = sqlite3.connect(os.path.abspath(database_path))
cursor = conn.cursor()

# Function to process a PDF file and return the extracted content
def process_pdf_file(file_path):
    """
    Process a PDF file and extract its text content.

    :param file_path: The path to the PDF file to be processed.
    :type file_path: str
    :return: The extracted text content of the PDF file, or None if an error occurs.
    :rtype: list of str or None
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            content = []
            for page in pdf.pages:
                content.append(page.extract_text())

            return content
    except (pdfplumber.PDFSyntaxError, FileNotFoundError, IOError) as e:
        print(f"Error processing '{file_path}': {e}")
        return None

# Iterate through all PDF files in the specified directory (and subdirectories)
for root, dirs, files in os.walk(directory, topdown=True):
    for file in files:
        # Check if the file is a PDF file
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)
            content = process_pdf_file(os.path.abspath(file_path))
            
            if content is not None:
                # Create a valid table name from the file name
                table_name = "table_" + re.sub(r'\W+', '_', file.replace('.pdf', ''))

                # Create a new table for the PDF content
                cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (page_num INTEGER PRIMARY KEY, content TEXT)")

                # Insert the content into the table
                for i, page_content in enumerate(content):
                    cursor.execute(f"INSERT INTO {table_name} (page_num, content) VALUES (?, ?)", (i+1, page_content))

                # Commit the changes
                conn.commit()

# Close the database connection
conn.close()
