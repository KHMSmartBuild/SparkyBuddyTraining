# Import necessary modules
import logging
import sqlite3
from pathlib import Path
import pdfplumber

# Configure logging
logging.basicConfig(filename="pdf_processing.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the directory to search and the path to the database
directory = Path("C:/Users/User/OneDrive/Desktop/training/Electrician")
database_path = Path("C:/Users/User/OneDrive/Desktop/Buisness/KHM Smart Build/Projects/Training data/Sparky training/databases/knowledge_base.db")

# Define a function to create the database schema
def create_database_schema(db_conn):
    db_conn.execute(
        "CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, pdf_file TEXT, page_num INTEGER, image_name TEXT, width INTEGER, height INTEGER)"
    )
    db_conn.commit()

# Define a function to process a PDF file and save its contents to the database
def process_pdf_file(file_path, db_conn):
    try:
        # Open the PDF file
        with pdfplumber.open(file_path) as pdf:
            
            # Create the cursor outside of the loop
            cursor = db_conn.cursor()

            # Iterate through all pages in the PDF file
            for page_num, page in enumerate(pdf.pages):
                # Extract and process text content
                text = page.extract_text()
                
                #TODO: Add specific processing logic here to save text to the database
                
                # Extract and process images
                images = page.images
                for img in images:
                    # Check if the image information already exists in the database
                    cursor.execute(
                        "SELECT id FROM images WHERE pdf_file=? AND page_num=? AND image_name=? LIMIT 1",
                        (str(file_path), page_num, img["name"])
                    )
                    row = cursor.fetchone()
                    if row is not None:
                        # Skip inserting duplicate row
                        continue

                    # Save image information to the database
                    cursor.execute(
                        "INSERT INTO images (pdf_file, page_num, image_name, width, height) VALUES (?, ?, ?, ?, ?)",
                        (str(file_path), page_num, img["name"], img["width"], img["height"]),
                    )
            
            # Log that the file was processed successfully
            logging.info(f"Processed '{file_path}' successfully.")

    # Catch any errors that may occur while processing the PDF file
    except Exception as e:
        # Log the error message
        logging.error(f"Error processing '{file_path}': {e}")

    return

# Connect to the database
conn = sqlite3.connect(database_path)

# Create the database schema
create_database_schema(conn)

# Iterate through all PDF files in the specified directory (and subdirectories)
for file_path in directory.rglob("*.pdf"):
    # Process the PDF file and save its contents to the database
    process_pdf_file(file_path, conn)
    
# Commit the changes and close the database connection
conn.commit()
conn.close()
