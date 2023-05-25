# Script name: data_cleaning_process.py
# Location: gui\data_cleaning_process.py
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
# Purpose:
"""
The purpose of this script is to clean the data from the conversation logs.
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.utils.Prep.preprocessing import (
    remove_punctuation,
    remove_numbers,
    to_lower,
    preprocess_text,
    preprocess_data,
    remove_stopwords,
    lemmatize_text
)

class CleaningFunctionWidget(QWidget):
    """
    Widget for selecting and applying cleaning functions to input data.
    """
    def __init__(self):
        super().__init__()

        # Create the layout for the widget
        layout = QHBoxLayout(self)

        # Initialize cleaning functions list
        self.cleaning_functions = []

        # Create a combo box for selecting functions
        self.combo_function = QComboBox()
        layout.addWidget(self.combo_function)

        # Create a text edit widget for displaying data previews
        self.data_preview = QTextEdit()
        layout.addWidget(self.data_preview)

        # Create a preview button for displaying data previews
        preview_btn = QPushButton("Preview")
        layout.addWidget(preview_btn)
        preview_btn.clicked.connect(self.preview_data)

        # Add cleaning function options to combo box
        self.combo_function.addItem("Remove Punctuation")
        self.combo_function.addItem("Remove Stop Words")
        self.combo_function.addItem("Lemmatize")
        self.combo_function.addItem("Remove Numbers")
        self.combo_function.addItem("To Lower")
        self.combo_function.addItem("Preprocess Text")
        self.combo_function.addItem("Preprocess Data")

        # Create buttons for adding/removing cleaning functions
        self.btn_plus = QPushButton("+")
        layout.addWidget(self.btn_plus)
        self.btn_minus = QPushButton("-")
        layout.addWidget(self.btn_minus)

        # Connect button signals to add/remove functions
        self.btn_plus.clicked.connect(self.add_function)
        self.btn_minus.clicked.connect(self.remove_function)

    def preview_data(self):
        """
        Displays a preview of the input data after applying cleaning functions.
        """
        sample_data = self.get_sample_data()
        self.data_preview.setText(sample_data)

    def get_sample_data(self):
        """
        Returns sample input data for preview purposes.
        """
        return "Sample data"

    def add_function(self):
        """
        Adds a new cleaning function widget to the layout.
        """
        new_function_widget = CleaningFunctionWidget()
        self.cleaning_functions.append(new_function_widget)
        self.layout().addWidget(new_function_widget)

    def remove_function(self):
        """
        Removes the current cleaning function widget from the layout.
        """
        self.cleaning_functions.remove(self)
        self.layout().removeWidget(self)
        self.deleteLater()

    def apply_cleaning_functions(self, input_data):
        """
        Applies the selected cleaning functions to the input data.
        """
        data = [input_data]

        # Validate input data
        if not self.validate_data(data):
            QMessageBox.warning(self, "Warning", "The cleaned data is not valid.")
            return None

        # Apply selected cleaning functions to input data
        for function_widget in self.cleaning_functions:
            selected_function = function_widget.combo_function.currentText()
            if selected_function == "Remove Punctuation":
                data = remove_punctuation(data)
            elif selected_function == "Remove Stop Words":
                data = remove_stopwords(data)
            elif selected_function == "Lemmatize":
                data = lemmatize_text(data)
            elif selected_function == "Remove Numbers":
                data = remove_numbers(data)
            elif selected_function == "To Lower":
                data = to_lower(data)
            elif selected_function == "Preprocess Text":
                data = preprocess_text(data)
            elif selected_function == "Preprocess Data":
                data = preprocess_data(data)

        return data[0]
    
    def validate_data(self, data):
        return bool(data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    function_widget = CleaningFunctionWidget()
    main_window.setCentralWidget(function_widget)
    main_window.show()
    sys