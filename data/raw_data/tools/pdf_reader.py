import sqlite3
import io
import tempfile
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter, ImageWriter
from pdfminer.layout import LAParams, LTImage
from PyPDF2 import PdfReader

# Define the database file name
database_file = 'electrical_database.db'

# Define the PDF reader class
class PDFReader:
    def __init__(self):
        self.conn = sqlite3.connect(database_file)
        
    def extract_data(self, pdf_path):
        # Load the PDF file
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PdfReader(pdf_file)

        # Extract text and images from each page
        for page in range(len(pdf_reader.pages)):
            # Extract text from the page
            text = self.extract_text_from_page(pdf_file, page)

            # Extract images from the page
            images = self.extract_images_from_page(pdf_file, page)

            # Insert the page data into the database
            self.insert_data(text, images)

        pdf_file.close()
        self.conn.commit()

    def extract_text_from_page(self, pdf_file, page_number):
        # Create a PDF resource manager object and set its parameters
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        pdf_reader = PdfReader(pdf_file)

        # Create a PDF interpreter object and set its parameters
        interpreter = PDFPageInterpreter(resource_manager, TextConverter(resource_manager, fake_file_handle, codec=codec, laparams=laparams))

        # Process the page
        page = pdf_reader.pages[page_number]
        interpreter.process_page(page)
        text = fake_file_handle.getvalue()

        # Close the fake file handle
        fake_file_handle.close()

        return text

    def extract_images_from_page(self, pdf_file, page_number):
        images = []
        writer = ImageWriter('images/')
        pdf_reader = PdfReader(pdf_file)

        # Extract images from the page
        page = pdf_reader.pages[page_number]
        for obj in page['/Resources']['/XObject'].values():
            if obj['/Subtype'] == '/Image':
                # Get the image data and type
                data = obj.getData()
                if 'JFIF' in data:
                    img_type = 'jpg'
                elif 'PNG' in data:
                    img_type = 'png'
                else:
                    img_type = 'bmp'

                # Write the image to a file and save its path
                with tempfile.NamedTemporaryFile(delete=False, suffix='.'+img_type) as f:
                    f.write(data)
                    img_path = f.name
                    images.append(img_path)

                    # Save the image path to the database
                    paragraph_id = self.insert_paragraph('', None)
                    self.insert_image(img_path, paragraph_id)

                    # Rename the file to its SHA256 hash
                    hash = writer.export_image(img_path)
                    os.rename(img_path, os.path.join('images', hash+'.'+img_type))

                    return images

    def insert_data(self, text, images):
        chapter_title, section_title, paragraph_text, definition_text, example_text, question_text, answer_text = None, None, None, None, None, None, None

        # Parse the page text to extract the relevant data
        for line in text.split('\n'):
            if line.startswith('Chapter'):
                chapter_title = line[8:]
            elif line.startswith('Section'):
                section_title = line[8:]
            elif line.startswith('Paragraph'):
                paragraph_text = line[8:]
            elif line.startswith('Definition'):
                definition_text = line[8:]
            elif line.startswith('Example'):
                example_text = line[8:]
            elif line.startswith('Question'):
                question_text = line[8:]
            elif line.startswith('Answer'):
                answer_text = line[8:]

            # Insert the chapter data into the database
            chapter_id = self.insert_chapter(chapter_title)  
            # Insert the section data into the database
            section_id = self.insert_section(chapter_id, section_title)
            # Insert the paragraph data into the database
            paragraph_id = self.insert_paragraph(chapter_id, section_id, paragraph_text)
            # Insert the definition data into the database
            definition_id = self.insert_definition(chapter_id, section_id, paragraph_id, definition_text)
            # Insert the example data into the database 
            example_id = self.insert_example(chapter_id, section_id, paragraph_id, example_text)
            # Insert the question data into the database
            question_id = self.insert_question(chapter_id, section_id, paragraph_id, question_text)
            # Insert the answer data into the database
            answer_id = self.insert_answer(chapter_id, section_id, paragraph_id, question_id, answer_text)

            # Insert the images data into the database
            for img_path in images:
                self.insert_image(img_path, chapter_id, section_id, paragraph_id)

            # Insert the text data into the database
            self.insert_text(chapter_id, section_id, paragraph_id, text)

        self.conn.commit()

    def get_thumbnail(self, pdf_path, page_number, size=(256,256)):
        pdf_file = open(pdf_path, 'rb')
        pdf_reader = PdfReader(pdf_file)

        # Extract the thumbnail image
        thumbnail = pdf_reader.pages[page_number].thumbnail(size)

        # Close the PDF file
        pdf_file.close()

        return thumbnail

       