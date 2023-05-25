import unittest
import os
import sys
from PyQt5 import QtWidgets, QtCore, QtGui

# Import the class to be tested
from Sparky_gui import SparkyGUI


class TestSparkyGui(unittest.TestCase):
    
    def test_initialization(self):
        app = QtWidgets.QApplication(sys.argv)
        window = SparkyGUI()
        
        # Testing the initialization of SparkyGUI
        self.assertEqual(window.windowTitle(), "Sparky - AI Electrician Assistant")
        self.assertEqual(window.geometry(), QtCore.QRect(100, 100, 1000, 800))

        # Testing the MainWindow widget of SparkyGUI
        self.assertIsInstance(window.centralWidget(), QtWidgets.QWidget)

        # Testing the chat_interface layout
        chat_interface_layout = window.centralWidget().layout().itemAt(0)
        self.assertIsInstance(chat_interface_layout, QtWidgets.QVBoxLayout)

        self.assertIsInstance(window.conversation_widget, QtWidgets.QTextEdit)
        self.assertIsInstance(window.user_input_widget, QtWidgets.QTextEdit)
        self.assertIsInstance(chat_interface_layout.itemAt(0).widget(), QtWidgets.QTextEdit)
        self.assertIsInstance(chat_interface_layout.itemAt(1).widget(), QtWidgets.QPushButton)

        # Testing the Dashboard layout
        dashboard_layout = window.centralWidget().layout().itemAt(1)
        self.assertIsInstance(dashboard_layout, QtWidgets.QHBoxLayout)

        for i in range(1, 9):
            self.assertIsInstance(dashboard_layout.itemAt(i).widget(), QtWidgets.QPushButton)

        # Testing the Tabbed Interface layout
        tab_widget = window.centralWidget().layout().itemAt(2).widget()
        self.assertIsInstance(tab_widget, QtWidgets.QTabWidget)

        # Testing the Image Tab layout
        image_tab_layout = tab_widget.widget(0).layout()
        self.assertIsInstance(image_tab_layout, QtWidgets.QVBoxLayout)

        self.assertIsInstance(image_tab_layout.itemAt(0).widget(), QtWidgets.QPushButton)
        self.assertIsInstance(image_tab_layout.itemAt(1).widget(), QtWidgets.QPushButton)

        # Testing the Media Tab layout
        media_tab_layout = tab_widget.widget(1).layout()
        media_controls_layout = media_tab_layout.itemAt(1)
        self.assertIsInstance(media_tab_layout, QtWidgets.QVBoxLayout)
        self.assertIsInstance(media_controls_layout, QtWidgets.QHBoxLayout)

        for i in range(0, media_controls_layout.count()):
            self.assertIsInstance(media_controls_layout.itemAt(i).widget(), QtWidgets.QPushButton)

        # Testing the Notes Tab layout
        notes_tab_layout = tab_widget.widget(2).layout()
        self.assertIsInstance(notes_tab_layout, QtWidgets.QVBoxLayout)

        self.assertIsInstance(notes_tab_layout.itemAt(0).widget(), QtWidgets.QTextEdit)
        notes_controls_layout = notes_tab_layout.itemAt(1)
        self.assertIsInstance(notes_controls_layout, QtWidgets.QHBoxLayout)

        for i in range(0, notes_controls_layout.count()):
            self.assertIsInstance(notes_controls_layout.itemAt(i).widget(), QtWidgets.QPushButton)

        # Testing the File Management Tab
        file_management_tab = tab_widget.widget(3)
        self.assertIsInstance(file_management_tab, QtWidgets.QWidget)

        # Testing the AITraining Console Tab
        ai_training_tab = tab_widget.widget(4)
        self.assertIsInstance(ai_training_tab, QtWidgets.QWidget)

        # Testing the Doodle Tab
        doodle_tab = tab_widget.widget(5)
        self.assertIsInstance(doodle_tab, QtWidgets.QWidget)


if __name__ == "__main__":
    unittest.main()
