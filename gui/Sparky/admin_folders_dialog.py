# Script name : admin_folders_dialog.py
# Location = gui\utils\prep\admin_folders_dialog.py
# Author: KHM Smartbuild
# Purpose: 
"""
This script creates the UI for the admin folders dialog.
It initializes the admin_folders_dialog UI.

"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
import os
import sqlite3
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit, QGridLayout, QApplication
from PyQt5.QtCore import Qt

class AdminFoldersDialog(QDialog):
    def __init__(self, db_path):
        super().__init__()
        # Connect to the SQLite database
        self.conn = sqlite3.connect(db_path)

        layout = QVBoxLayout()
        layout = QVBoxLayout()
        label = QLabel("Manage and create admin folders here.")
        layout.addWidget(label)

        grid_layout = QGridLayout()
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        layout.addWidget(self.console_output)

        self.console_input = QLineEdit()
        self.console_input.returnPressed.connect(self.handle_command)
        layout.addWidget(self.console_input)

        self.retrieve_button = QPushButton("Retrieve Files")
        self.retrieve_button.clicked.connect(self.retrieve_files)
        grid_layout.addWidget(self.retrieve_button, 0, 0)

        self.update_button = QPushButton("Update Files")
        self.update_button.clicked.connect(self.update_files)
        grid_layout.addWidget(self.update_button, 0, 1)

        layout.addLayout(grid_layout)
        self.setLayout(layout)

    def handle_command(self):
        command = self.console_input.text()
        self.console_input.clear()
        if command == "list":
            # Code to list files in the admin folder
            self.console_output.append("List of files in admin folder")
        elif command.startswith("delete "):
            # Code to delete a file from the admin folder
            filename = command[len("delete "):]
            self.console_output.append(f"Deleted file: {filename}")
        else:
            self.console_output.append("Invalid command")
            self.console_output.append("Command: " + command)

    def retrieve_files(self):
        try:
            db_files = self.db.retrieve_files()
            self.console_output.append("Retrieve Files button pressed")
            return db_files
        except Exception as e:
            self.console_output.append(f"Error retrieving files: {str(e)}")

    def update_files(self):
        try:
            self.db.update_files()
            self.console_output.append("Update Files button pressed")
        except Exception as e:
            self.console_output.append(f"Error updating files: {str(e)}")
