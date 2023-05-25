import sys
import os
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFrame, QScrollArea, QWidget, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QImageReader
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class ImageGenerator(QMainWindow):
    def __init__(self):
        super().__init__()


        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Prompt input
        prompt_layout = QHBoxLayout()
        layout.addLayout(prompt_layout)

        self.prompt_entry = QLineEdit(self)
        self.prompt_entry.setPlaceholderText("Enter a prompt")
        prompt_layout.addWidget(self.prompt_entry)

        self.prompt_help_button = QPushButton("?", self)
        self.prompt_help_button.clicked.connect(self.show_prompt_help)
        prompt_layout.addWidget(self.prompt_help_button)

        # Image display
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        # Generate image button
        generate_image_button = QPushButton("Generate Image", self)
        generate_image_button.clicked.connect(self.generate_image)
        layout.addWidget(generate_image_button)

    def display_image(self, image_url):
        response = requests.get(image_url)
        image_data = response.content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def generate_image(self):
        prompt = self.prompt_entry.text()
        for keyword_category in self.keyword_checkbuttons:
            for checkbutton in self.keyword_checkbuttons[keyword_category]:
                if checkbutton.isChecked():
                    prompt += f" {checkbutton.text()}"   
                     
        if not self.validate_input(prompt):
            return
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response['data'][0]['url']
            self.display_image(image_url)
        except Exception as e:
            QMessageBox.critical(self, "Error", "An error occurred while generating the image. Please try again later.")
            print(e)

    def validate_input(self, prompt):
        if len(prompt) == 0:
            QMessageBox.critical(self, "Error", "Please enter a prompt.")
            return False
        return True

    def show_prompt_help(self):
        QMessageBox.information(self, "Prompt Help",
                                "Provide a detailed description to get better results."
                                "Example prompts:"
                                "  - a white Siamese cat"
                                "  - a close up, studio photographic portrait of a white Siamese cat that looks curious, backlit ears")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    image_generator = ImageGenerator()
    image_generator.show()
    sys.exit(app.exec_())
