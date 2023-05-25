import os
import sqlite3
from PIL import Image

# Import pdfplumber and check if it exists
try:
    import pdfplumber
except ImportError:
    print("pdfplumber library is not installed. Please install it using 'pip install pdfplumber'")

# Define the directory to search
directory = r"C:\Users\User\OneDrive\Desktop\training\Electrician"
database_path = r"databases\knowledge_base.db"

# Function to process a PDF file and extract text and images
def process_pdf_file(file_path: str, db_conn: sqlite3.Connection) -> None:
    """
    Processes a PDF file, extracting its text content and images and saving them to a database.
    :param file_path: The path to the PDF file to process.
    :param db_conn: The database connection to use for saving the extracted content.
    :return: None if there was an error processing the file, otherwise, the extracted content is saved to the database.
    :raises pdfplumber.PDFSyntaxError: If there was an error parsing the PDF file.
    :raises FileNotFoundError: If the PDF file could not be found.
    :raises IOError: If there was an error reading the PDF file.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Extract and process text content
                text = page.extract_text()
                # Process the text content (e.g., save it to a database)
                # Add your specific processing logic here

                # Extract and process images
                images = page.images
                for img in images:
                    # Save the image using PIL
                    image_path = f"{os.path.splitext(os.path.basename(file_path))[0]}_page{page_num}_image{img['name']}.png"
                    if 'data' in img:
                     Image.frombytes("RGBA", (img['width'], img['height']), img['data']).save(image_path)


                    # Save image information to the database
                    db_conn.execute("INSERT INTO images (pdf_file, page_num, image_name, image_path) VALUES (?, ?, ?, ?)",
                                    (file_path, page_num, img['name'], image_path))
                    db_conn.commit()

    except (Exception, FileNotFoundError, IOError) as e:
        print(f"Error processing '{file_path}': {e}")
        return None

# Connect to the database
conn = sqlite3.connect(database_path)
# Create table with columns for PDF file, page_num, image_name, and image_path
conn.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, pdf_file TEXT, page_num INTEGER, image_name TEXT, image_path TEXT)")
conn.commit()

# Iterate through all PDF files in the specified directory (and subdirectories)
for root, dirs, files in os.walk(directory, topdown=True):
    for file in files:
        # Check if the file is a PDF file
        if file.endswith('.pdf'):
            file_path = os.path.join(root, file)
            process_pdf_file(file_path, conn)

# Close the database connection
conn.close()
