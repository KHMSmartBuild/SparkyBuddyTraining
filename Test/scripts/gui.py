import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import re
import openai
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from dotenv import load_dotenv
from hf_tools.agents.question_makergpt2 import generate_text

from utils.prep.file_conversion import convert_file
from utils.prep.preprocessing import preprocess_data
from utils.prep.save_data import save_data

load_dotenv()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat with Sparky")

        # Create a main widget to hold the other widgets
        main_widget = QFrame(self)
        main_widget.setFrameStyle(QFrame.Box)
        self.setCentralWidget(main_widget)

        # Create a vertical layout for the main widget
        main_layout = QVBoxLayout(main_widget)

        # Create input field
        self.user_input = QLineEdit()
        main_layout.addWidget(self.user_input)

        # Create submit button
        self.submit_button = QPushButton("Submit")
        main_layout.addWidget(self.submit_button)

        # Create text area for displaying the conversation
        self.conversation = QTextEdit()
        main_layout.addWidget(self.conversation)

        # Create a horizontal layout for the file selection button and the Whimsical chart button
        button_layout = QHBoxLayout()

        # Create a button to select a file
        self.select_file_button = QPushButton("Select File")
        button_layout.addWidget(self.select_file_button)

        # Create a button to open the Whimsical chart viewer
        self.open_whimsical_button = QPushButton("Open Whimsical Chart")
        button_layout.addWidget(self.open_whimsical_button)

        # Add the button layout to the main layout
        main_layout.addLayout(button_layout)

        # Create a button to open the chat window
        self.open_chat_window_button = QPushButton("Open Chat Window")
        main_layout.addWidget(self.open_chat_window_button)

        # Connect the button signals to their respective slots
        self.submit_button.clicked.connect(self.submit)
        self.select_file_button.clicked.connect(self.select_file)
        self.open_whimsical_button.clicked.connect(self.open_whimsical_window)
        self.open_chat_window_button.clicked.connect(self.open_chat_window)

        # Create a text box to display the preprocessed data
        self.text_box = QTextEdit()
        main_layout.addWidget(self.text_box)

    def submit(self):
        # Handle user input and model response here
        pass

    def select_file(self):
        """
        Allows the user to select a file and process the data.

        Returns:
            None
        """
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        self.process_and_display_data(file_path)

    def process_and_display_data(self, file_path):
        """
        Preprocesses the data, updates the text box with the preprocessed data, and saves the preprocessed data to a file.

        Args:
            file_path (str): The path of the file to preprocess.

        Returns:
            None
        """
        # Convert the file to text
        raw_text = convert_file(file_path)

        # Preprocess the text
        preprocessed_text = preprocess_data(raw_text)

        # Update the text box with the preprocessed text
        self.text_box.clear()
        self.text_box.insertPlainText(preprocessed_text)

        # Save the preprocessed text to a file
        output_directory = 'dataset'
        output_filename = 'preprocessed_data.txt'
        save_data(preprocessed_text, output_directory, output_filename)

    def create_whimsical_iframe(self, url):
        """
        Creates an HTML iframe to display a Whimsical chart.

        Args:
        url (str): The URL of the Whimsical chart.

    Returns:
        str: An HTML iframe that displays the Whimsical chart.
    """
    match = re.search(r'(https:\/\/)?whimsical.com\/(?:[a-zA-Z0-9\-]+\-)?([a-km-zA-HJ-NP-Z1-9]{16,22})(@[a-km-zA-HJ-NP-Z1-9]+)?', url)
    if match:
        whimsical_id = match.group(2)
        iframe_html = f'<iframe style="border:none" src="https://whimsical.com/embed/{whimsical_id}" width="800" height="450"></iframe>'
        return iframe_html
    

    def open_whimsical_window(self):
        """
        Opens a new window to display the Whimsical chart.

        Returns:
            None
        """
        # Added closing quotation mark at the end of the URL
        whimsical_url = "https://whimsical.com/sparky-buddy-training-LM"
        iframe_html = self.create_whimsical_iframe(whimsical_url)
        if iframe_html:
            # Create the window and set the title
            win = QMainWindow()
            win.setWindowTitle("Sparky Buddy Training")

            # Create the html frame and set its content
            iframe = QFrame(win)
            iframe.setFrameStyle(QFrame.Box)
            iframe.setLineWidth(0)
            iframe.setMidLineWidth(0)
            iframe_layout = QVBoxLayout(iframe)
            iframe_content = QTextEdit()
            iframe_content.setHtml(iframe_html)
            iframe_content.setReadOnly(True)
            iframe_layout.addWidget(iframe_content)
            win.setCentralWidget(iframe)

            # Set the size of the window and show it
            win.resize(800, 450)
            win.show()

    def open_chat_window(self):
        """
        Opens a new window for the user to enter text and receive a response.

        Returns:
            None
        """
        chat_window = QMainWindow()
        chat_window.setWindowTitle("Chat with Sparky Buddy")

        chat_text = QTextEdit(chat_window)
        chat_text.setReadOnly(True)
        chat_window.setCentralWidget(chat_text)

        user_entry = QLineEdit(chat_window)

        def send_message():
            """
            Sends the user's message to the OpenAI API and displays the response in the chat_text widget.

            Returns:
                None
            """
            user_message = user_entry.text().strip()
            chat_text.insertPlainText("You: " + user_message + "\n")
            user_entry.clear()

            # Generate a response using the OpenAI API
            response = generate_text(user_message)
            chat_text.insertPlainText("Sparky Buddy: " + response + "\n")
            chat_text.moveCursor(QTextCursor.End)

        submit_button = QPushButton(chat_window)
        submit_button.setText("Send")
        submit_button.clicked.connect(send_message)

        # Create a horizontal layout for the input field and the submit button
        input_layout = QHBoxLayout()
        input_layout.addWidget(user_entry)
        input_layout.addWidget(submit_button)

        # Create a vertical layout for the chat window and add the input layout and the chat text widget to it
        chat_layout = QVBoxLayout(chat_window)
        chat_layout.addLayout(input_layout)
        chat_layout.addWidget(chat_text)

        # Set the size of the window and show it
        chat_window.resize(500, 500)
        chat_window.show()
    if name == 'main': app = QApplication(sys.argv)
    window = MainWindow() 
    window.resize(800, 600) 
    window.show() 
    sys.exit(app.exec_())

