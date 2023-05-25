from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel

class ScheduleTasksDialog(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("Schedule tasks and appointments here.")
        layout.addWidget(label)

        self.setLayout(layout)

