import sqlite3

class BS7671DataLoader:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        
    def get_chapters(self):
        """
        Returns a list of tuples representing the chapters in the BS7671 standard. Each tuple contains the chapter ID
        and chapter title.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT chapter_id, chapter_title FROM Chapters")
        return cursor.fetchall()

    def get_sections(self, chapter_id):
        """
        Returns a list of tuples representing the sections in the specified chapter. Each tuple contains the section ID,
        section title, and chapter ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT section_id, section_title, chapter_id FROM Sections WHERE chapter_id = ?", (chapter_id,))
        return cursor.fetchall()

    def get_paragraphs(self, section_id):
        """
        Returns a list of tuples representing the paragraphs in the specified section. Each tuple contains the paragraph
        ID, paragraph text, and section ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT paragraph_id, paragraph_text, section_id FROM Paragraphs WHERE section_id = ?", (section_id,))
        return cursor.fetchall()

    def get_images(self, paragraph_id):
        """
        Returns a list of tuples representing the images associated with the specified paragraph. Each tuple contains the
        image ID, image path, and paragraph ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT image_id, image_path, paragraph_id FROM Images WHERE paragraph_id = ?", (paragraph_id,))
        return cursor.fetchall()

    def get_definitions(self):
        """
        Returns a list of tuples representing the definitions in the BS7671 standard. Each tuple contains the definition
        ID, term, and definition text.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT definition_id, term, definition_text FROM Definitions")
        return cursor.fetchall()

    def get_examples(self, paragraph_id):
        """
        Returns a list of tuples representing the examples associated with the specified paragraph. Each tuple contains
        the example ID, example text, and paragraph ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT example_id, example_text, paragraph_id FROM Examples WHERE paragraph_id = ?", (paragraph_id,))
        return cursor.fetchall()

    def get_questions(self, section_id):
        """
        Returns a list of tuples representing the questions associated with the specified section. Each tuple contains
        the question ID, question text, and section ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT question_id, question_text, section_id FROM Questions WHERE section_id = ?", (section_id,))
        return cursor.fetchall()

    def get_answers(self, question_id):
        """
        Returns a list of tuples representing the answers associated with the specified question. Each tuple contains
        the answer ID, answer text, and question ID.
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT answer_id, answer_text, question_id FROM Answers WHERE question_id = ?", (question_id,))
        return cursor.fetchall()

    def close(self):
        """
        Closes the connection to the database.
        """
        self.conn.close()