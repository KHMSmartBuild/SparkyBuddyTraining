from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class ProjectFoldersDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("Manage project folders here.")
        layout.addWidget(label)

        self.setLayout(layout)
