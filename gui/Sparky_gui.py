# Script name : Sparky_gui.py
# location = gui\Sparky_gui.py
# accessable from Libraries = #TODO implement libraries
# Author: KHM Smartbuild
# Purpose: This script is used to create the GUI for training AI electrician assistant Sparky and the Buddy agents in the system.
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import keyboard

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, 'utils'))
import speech_recognition as sr
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, QTabWidget
from gui.Sparky.ai_task_management import AITaskManagement
from gui.Sparky.admin_folders_dialog import AdminFoldersDialog
from gui.Sparky.image_create import ImageGenerator
from gui.Sparky.Sparky_image_editor import ImageEditor
from gui.Sparky.project_folders_dialog import ProjectFoldersDialog
from gui.Sparky.quote_tasks_dialog import QuoteTasksDialog
from gui.Sparky.schedule_tasks_dialog import ScheduleTasksDialog
from gui.Sparky.data_cleaning_process import CleaningFunctionWidget
from gui.Sparky.sparky_chat import SparkyChat
from gui.utils.Prep.doodle_sketch_pad import DoodleSketchPad
from gui.utils.Prep.file_management import FileManager
from gui.utils.Prep.media_tab import MediaTab
from gui.utils.Prep.video_processor import VideoProcessorGUI, VideoProcessor
from gui.utils.connect_to_IoT_device import IotDeviceWindow
import platform
import ctypes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(r'C:\Users\User\OneDrive\Desktop\Buisness\KHM Smart Build\Projects\Training data\Sparky  training\Test\Logs\sparky_gui_training.log', maxBytes=2000, backupCount=5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class SparkyGUI(QMainWindow):
    def __init__(self):
        """
        Initializes the SparkyGUI class which is a graphical user interface for the AI electrician 
        assistant called Sparky. It sets the window title, geometry and central widget. 
        It creates a chat interface that consists of a QTextEdit widget for conversation and a separate widget for user input. 
        It also adds a send button for user input and sets a read-only property for the conversation_widget. 
        It creates a dashboard which contains several buttons for various tasks such as speech to text controls, quotes,
        schedule tasks, project folders, admin folders, IoT, user preferences, and API integration. 
        It adds a Clean Data button to the dashboard layout. 
        It initializes a keywords dictionary that consists of categories and their respective values. 
        It creates a tabbed interface that consists of four tabs: Image studio, Media, Notes, File Management, 
        AI Training Console, and Doodle. 
        It creates an instance of SparkyChat to generate chat responses.
        """
        super().__init__()
        self.setWindowTitle("Sparky - AI Electrician Assistant")
        self.setGeometry(100, 100, 1000, 800)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        logging.info("Sparky GUI initialized")
        # Chat Interface
        chat_layout = QVBoxLayout()
        self.conversation_widget = QTextEdit()
        self.conversation_widget.setPlaceholderText("Conversation with Sparky")
        self.conversation_widget.setReadOnly(True)  # Make conversation_widget read-only
        chat_layout.addWidget(self.conversation_widget)
        self.user_input_widget = QTextEdit()  # Add a separate widget for user input
        self.user_input_widget.setPlaceholderText("Type your message here")
        chat_layout.addWidget(self.user_input_widget)
        # Add a send button for user input
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.handle_user_input)
        keyboard.add_hotkey('enter', self.handle_user_input)
        chat_layout.addWidget(send_btn)
        main_layout.addLayout(chat_layout)
        logging.info("Sparky GUI created")
        # Dashboard
        dashboard = QHBoxLayout()
        # Add a speech to text controls for user input
        start_speech_btn = QPushButton("Start Speech to Text")
        start_speech_btn.clicked.connect(self.submit_voice_query)
        keyboard.add_hotkey('Ctrl + Shift + S', self.submit_voice_query)
        dashboard.addWidget(start_speech_btn)   
        send_btn.clicked.connect(self.handle_user_input)
        dashboard.addWidget(send_btn)
        Quotes_btn = QPushButton("Quotes")
        Quotes_btn.clicked.connect(self.show_quote_tasks_dialog)
        dashboard.addWidget(Quotes_btn)
        schedule_tasks_btn = QPushButton("Schedule Tasks")
        schedule_tasks_btn.clicked.connect(self.show_schedule_tasks_dialog)
        dashboard.addWidget(schedule_tasks_btn)
        project_folders_btn = QPushButton("Project Folders")
        project_folders_btn.clicked.connect(self.show_project_folders_dialog)
        dashboard.addWidget(project_folders_btn)
        admin_folders_btn = QPushButton("Admin Folders")
        admin_folders_btn.clicked.connect(self.show_admin_folders_dialog)
        dashboard.addWidget(admin_folders_btn)
        iot_btn = QPushButton("IoT")
        iot_btn.clicked.connect(self.connect_to_iot_device)
        dashboard.addWidget(iot_btn)
        user_pref_btn = QPushButton("User Preferences")
        dashboard.addWidget(user_pref_btn)
        api_integration_btn = QPushButton("API Integration")
        dashboard.addWidget(api_integration_btn)
        clean_data_button = QPushButton("Clean Data")
        clean_data_button.clicked.connect(self.open_data_cleaning_gui)
        dashboard.addWidget(clean_data_button)  
        main_layout.addLayout(dashboard)
        logging.info("Sparky dashboard created")
        self.keywords = open("gui/Sparky/image_prompt_keywords.py", "r").read()
        logging.info("Keywords loaded")
        # Tabbed Interface
        tab_widget = QTabWidget()
        # Image Tab
        image_tab = QWidget()
        image_layout = QVBoxLayout()
        image_tab.setLayout(image_layout)
        tab_widget.addTab(image_tab, "Image studio")
        main_layout.addWidget(tab_widget)
        self.image_generator_button = QPushButton("Open Image Generator", self)
        self.image_generator_button.clicked.connect(self.open_image_generator)
        image_layout.addWidget(self.image_generator_button)
        self.image_editor_button = QPushButton("Open Image Editor", self)
        self.image_editor_button.clicked.connect(self.open_image_editor)
        image_layout.addWidget(self.image_editor_button)
        logging.info("Image tab created")
        # Media Tab
        media_tab = MediaTab()
        media_tab_layout = QVBoxLayout()
        media_tab.setLayout(media_tab_layout)
        tab_widget.addTab(media_tab, "Media")
        media_tab.add_media(FileManager("path/to/local/file.mp4"))
        media_tab.add_media(VideoProcessorGUI("different/path/to/local/file.mp4"))
       
        
        # Notes Tab
        notes_tab = QWidget()
        notes_layout = QVBoxLayout()
        notes_tab.setLayout(notes_layout)
        notes_editor = QTextEdit()
        notes_layout.addWidget(notes_editor)
        notes_controls = QHBoxLayout()
        save_button = QPushButton("Save")
        notes_controls.addWidget(save_button)     
        import_button = QPushButton("Import")
        notes_controls.addWidget(import_button)
        export_button = QPushButton("Export")
        notes_controls.addWidget(export_button)
        notes_layout.addLayout(notes_controls)
        tab_widget.addTab(notes_tab, "Notes")
        main_layout.addWidget(tab_widget)
        # File Management Tab
        file_management_tab = FileManager()
        tab_widget.addTab(file_management_tab, "File Management")
        # Task Management Tab
        AI_Training_Console_tab = AITaskManagement()
        tab_widget.addTab(AI_Training_Console_tab, "AI Training Console")
        # Doodle Tab
        doodle_tab = self.doodle_sketch_pad()
        tab_widget.addTab(doodle_tab, "Doodle")
        logging.info("Gui Tabs created")
        # Create an instance of SparkyChat
        sparky_chat = SparkyChat()
        logging.info("SparkyChat created")
        self.setLayout(main_layout)

    def keyPressEvent(self, event):
        """
        Handles a key press event. If the key pressed is the return key and the user input widget has focus,
        calls the handle_user_input method. Then, calls the keyPressEvent method of the superclass with the event 
        parameter. Finally, logs the creation of a new keyboard.

        :param event: A QKeyEvent object representing the key event.
        :return: None.
        """
        if event.key() == Qt.Key_Return and self.user_input_widget.hasFocus():
            self.handle_user_input()
        super().keyPressEvent(event)
        logging.info("Keyboard created")
    
    def handle_user_input(self):
        """
        Handles the user input in the chat interface and updates the conversation widget with Sparky's response.

        Parameters:
        self: The object pointer.
        
        Returns:
        None
        """
        user_input = self.user_input_widget.toPlainText().strip()
        if user_input:
            # Append the user input to the conversation
            self.conversation_widget.append(f"You: {user_input}")
            logging.info(f"You: {user_input}")
        # Transcribe speech to text if necessary
        if user_input.lower() == "voice input":
            user_input = self.speech_to_text()
            logging.info(f"User said: {user_input}")
        # Generate response from Sparky and update conversation widget
        sparky_response = self.sparky_chat.generate_chat_response(user_input)
        self.conversation_widget.append(f"Sparky: {sparky_response}")
        logging.info(f"Sparky: {sparky_response}")
        # Clear user_input_widget
        self.user_input_widget.clear()

    # define a function to add a response to the conversation
    def add_sparky_response(self, response):
        """
        Adds a response to the conversation widget with the speaker name 'Sparky'.

        Args:
            response (Any): The response to be added to the conversation widget.

        Returns:
            None: This function does not return anything.
        """
        self.conversation_widget.append(f"Sparky: {response}") if hasattr(self, "conversation_widget") else None

    # define a function to start speech to text
    def speech_to_text(self):
        """
        Convert speech input from the user to text using the microphone
        and Google Speech Recognition service.

        :return: A string representing the recognized user input.
        """
        recognizer = sr.Recognizer()
        user_input = ""
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            try:
                user_input = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                print("Error: Speech recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Error: Could not request results from Google Speech Recognition service; {e}")
        except OSError:
            print("Error: Microphone not working or not found")
        logging.info("Speech to text created","Speach to text is working")
        return user_input

    def submit_voice_query(self):
        """
        Executes a voice query submission by converting the user's voice input to text, 
        generating a chat response using SparkyChat, setting the user input widget with the response,
        and handling the user input. 

        Parameters:
        self (object): The object instance that the method operates on.

        Returns:
        None
        """
        logging.info("submit_voice_query called")
        user_input = self.speech_to_text()
        response = SparkyChat().generate_chat_response(user_input)
        self.user_input_widget.setText(response)
        self.handle_user_input()

    def open_data_cleaning_gui(self):
        """
        Creates and shows a dialog window for cleaning data. This function takes no parameters and
        returns nothing.
        """
        logging.info("open_data_cleaning_gui called")
        try:
            self.data_cleaning_window = self.CleaningFunctionWidget()
            self.data_cleaning_window.setWindowTitle("Data Cleaning")
        except Exception as e:
            logging.error(f"An error occurred in open_data_cleaning_gui: {e}")
        logging.info("open_data_cleaning_gui completed")
    def show_schedule_tasks_dialog(self):
        """
        Creates and shows a dialog window for managing schedule tasks. This function takes no parameters and
        returns nothing.
        """
        logging.info("show_schedule_tasks_dialog called")
        try:
            self.schedule_tasks_window = ScheduleTasksDialog()
            self.schedule_tasks_window.setWindowTitle("Schedule Tasks")
        except Exception as e:
            logging.error(f"An error occurred in show_schedule_tasks_dialog: {e}")
        logging.info("show_schedule_tasks_dialog completed")
        
    def show_project_folders_dialog(self):
        """
        Creates and shows a dialog window for managing project folders. This function takes no parameters and
        returns nothing.
        """
        logging.info("show_project_folders_dialog called")
        try:
            self.project_folders_window = ProjectFoldersDialog()
            self.project_folders_window.setWindowTitle("Project Folders")
        except Exception as e:
            logging.error(f"An error occurred in show_project_folders_dialog: {e}")
        logging.info("show_project_folders_dialog completed")
        
    def show_quote_tasks_dialog(self):
        """
        Creates and shows a dialog window for managing quote tasks. This function takes no parameters and
        returns nothing.

        :return: None
        """
        logging.info("show_quote_tasks_dialog called")
        try:
            self.quote_tasks_window = QuoteTasksDialog()
            self.quote_tasks_window.setWindowTitle("Quote Tasks")
        except Exception as e:
            logging.error(f"An error occurred in show_quote_tasks_dialog: {e}")
        logging.info("show_quote_tasks_dialog completed")

    def show_admin_folders_dialog(self):
        """
        Initializes and displays the Admin Folders dialog box. 

        Args:
            self: the instance of the current class.
        
        Returns:
            None.
        """
        self.admin_folders_window = AdminFoldersDialog()
        self.admin_folders_window.setWindowTitle("Admin Folders")
   
    def open_image_generator(self):
        """
        Initializes a new instance of the ImageGenerator class and displays it.
        """
        self.image_generator = ImageGenerator()
        self.image_generator.show()

    def connect_to_iot_device(self):
        """Connect to IoT device and open window"""
        # Create an instance of the IotDeviceWindow class
        self.IoT_device_window = IotDeviceWindow()
        # Show the window
        self.IoT_device_window.show()

    def process_video(self):
        """Process video using VideoProcessor class"""
        video_url = self.path_input.text()
        # Download the video and get its path
        video_path = self.download_video(video_url)
        # Process the video using VideoProcessor
        video_processor = VideoProcessor(video_path)
        video_processor.process()
        # Display the processed video using VideoProcessorGUI
        video_processor_gui = VideoProcessorGUI(video_processor)
        video_processor_gui.run()
 
    def doodle_sketch_pad(self):
        """
        Creates a DoodleSketchPad instance and returns it.

        If there is no touchscreen available, the function prints a message
        instructing the user to hold down 'Ctrl' to use the mouse pointer.
        After that, it waits for the 'ctrl' key to be pressed within 10 seconds.

        :param self: The object instance.
        :return: A DoodleSketchPad instance.
        """
        touchscreen = self.is_touchscreen_available()
        if not touchscreen:
            print("Touchscreen not available. Hold down 'Ctrl' to use the mouse pointer.")
            keyboard.wait('ctrl', timeout=10)
        return DoodleSketchPad(touchscreen=touchscreen).get_doodle()

    def get_input_device(self):
        """
        Returns a tuple. The first element is a boolean indicating whether a touchscreen is available.
        The second element is a string specifying which input device to use ("touchscreen" or "mouse").
        The function follows similar logic to `is_touchscreen_available`, but if a touchscreen is not available,
        the function will specify that the mouse should be used instead.
        """
        system = platform.system()
        if system == "Windows":
            try:
                touch_available = bool(ctypes.windll.user32.GetSystemMetrics(86))
                return (touch_available, "touchscreen" if touch_available else "mouse")
            except AttributeError:
                return (False, "mouse")
        elif system == "Linux":
            touch_available = "TOUCH" in os.popen("xinput list").read()
            return (touch_available, "touchscreen" if touch_available else "mouse")
        elif system == "Darwin":
            touch_available = "Touchscreen" in os.popen("ioreg -p IOUSB").read()
            return (touch_available, "touchscreen" if touch_available else "mouse")
        elif system == "Android":
            return (True, "touchscreen")
        else:
            return (False, "mouse")

    def send_doodle_to_Sparky(self, doodle, sparky):
        """
        Sends a given doodle to a Sparky instance.

        :param doodle: The doodle to be sent to the Sparky instance.
        :type doodle: Any
        :param sparky: The Sparky instance to receive the doodle.
        :type sparky: Any
        """
        # Send the doodle to the Sparky
        self.send_doodle_to_Sparky(doodle, self.sparky_chat)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SparkyGUI()
    window.show()
    sys.exit(app.exec_())
