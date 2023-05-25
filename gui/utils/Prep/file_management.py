import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QTreeView, QFileSystemModel
class FileManager(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Save file button
        save_button = QPushButton("Save File")
        save_button.clicked.connect(self.save_file_dialog)
        layout.addWidget(save_button)

        # Load file button
        load_button = QPushButton("Load File")
        load_button.clicked.connect(self.load_file_dialog)
        layout.addWidget(load_button)

        # Create directory button
        create_dir_button = QPushButton("Create Directory")
        create_dir_button.clicked.connect(self.create_directory_dialog)
        layout.addWidget(create_dir_button)

        # Delete file button
        delete_button = QPushButton("Delete File")
        delete_button.clicked.connect(self.delete_file_dialog)
        layout.addWidget(delete_button)

        # File browser
        self.file_browser = QTreeView()
        layout.addWidget(self.file_browser)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath('')  # Set the root path to the file system root
        self.file_browser.setModel(self.file_model)

        # Hide the Size, Type, and Date Modified columns
        self.file_browser.setColumnHidden(1, True)
        self.file_browser.setColumnHidden(2, True)
        self.file_browser.setColumnHidden(3, True)

        # Connect the file browser's selection to a method that handles file selection
        self.file_browser.selectionModel().selectionChanged.connect(self.handle_file_selection)


    def save_file_dialog(self):
        """Open a file save dialog and return the selected file path."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Save File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options)
        return file_path
    
    def load_file_dialog(self):
        """Open a file open dialog and return the selected file path."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Load File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options)
        return file_path
    
    def create_directory_dialog(self):
        """Open a directory creation dialog and create a directory at the selected path."""
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_path = QFileDialog.getExistingDirectory(None, "Create Directory", "", options=options)
        if dir_path:
            self.create_directory(dir_path)

    def delete_file_dialog(self):
        """Open a file open dialog, and delete the selected file."""
        file_path = self.load_file_dialog()
        if file_path:
            self.delete_file(file_path)

    def handle_file_selection(self, selected, deselected):
        # Get the selected index
        index = selected.indexes()[0]

        # Get the file path for the selected index
        file_path = self.file_model.filePath(index)

        # Perform any desired actions with the file_path, such as displaying file metadata
        pass