# Script name : Sparky_gpt4_UI.py
# Location = gui\Sparky_gpt4_UI.py
# Accessable from Libraries = #TODO implement libraries
# Author: KHM Smartbuild
# Purpose: TODO add this purpose
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
"""This is the Sparky GUI for Electricians
the GUI is created using streamlit
the features are:
- A chat interface that consists of a QTextEdit widget for conversation and a separate widget for user input
- A send button for user input
- A read-only property for the conversation_widget

logging can be found in the sparkyGpt4.log file

"""

import streamlit as st
from PIL import Image
import numpy as np
import cv2
from sparky_assistant_gpt4 import SparkyAssistantGPT4
import threading


# Define image processing function
def process_image(img_arr, kernel_size, canny_min, canny_max):
    # Gaussian Blur
    img_blur = cv2.GaussianBlur(img_arr, (kernel_size, kernel_size), 0)

    # Canny Edge Detection
    img_canny = cv2.Canny(img_arr, canny_min, canny_max)

    return img_blur, img_canny

# Define Sparky AI Assistant function
def sparky_assistant():
    sparky = SparkyAssistantGPT4()
    while True:
        user_input = st.text_input("Enter your question: ")
        if user_input:
            response = sparky.generate_response(user_input)
            st.write("Sparky: ", response)

# Streamlit app
def main():
    st.title("Image Processing and Sparky AI Assistant for Electricians")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "png"])

    # Check if image is uploaded
    if uploaded_file is not None:

        # Read image file directly into a NumPy array
        img_arr = cv2.imdecode(np.fromstring(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Display Original Image
        st.subheader("Original Image")
        cv2.imshow("Original Image", img_arr)

        # Get image processing parameters
        kernel_size = st.slider("Select kernel size for Gaussian blur", 1, 50, 1, 1)
        canny_min = st.slider("Select minimum threshold for Canny edge detection", 0, 255, 50, 1)
        canny_max = st.slider("Select maximum threshold for Canny edge detection", 0, 255, 150, 1)

        # Process Image
        img_blur, img_canny = process_image(img_arr, kernel_size, canny_min, canny_max)

        # Display Blurred Image
        st.subheader("Blurred Image")
        st.image(img_blur, channels="BGR")

        # Display Canny Image
        st.subheader("Canny Edge Detection Image")
        st.image(img_canny, channels="BGR")

    # Sparky AI Assistant
    st.subheader("Sparky AI Assistant")

    # Run Sparky AI Assistant in a separate thread
    sparky_thread = threading.Thread(target=sparky_assistant)
    sparky_thread.start()

# Embed HTML code for tabbed interface
html = '''
    <div class="tab">
      <button class="tablinks" onclick="openTab(event, 'DataCleaning')">Data Cleaning</button>
      <button class="tablinks" onclick="openTab(event, 'ScheduleTasks')">Schedule Tasks</button>
      <button class="tablinks" onclick="openTab(event, 'ProjectFolders')">Project Folders</button>
      <button class="tablinks" onclick="openTab(event, 'QuoteTasks')">Quote Tasks</button>
      <button class="tablinks" onclick="openTab(event, 'ConnectIOT')">Connect IoT Device</button>
    </div>

    <div id="DataCleaning" class="tabcontent">
      <h3>Data Cleaning</h3>
      <p>Open the data cleaning GUI</p>
      <button onclick="openDataCleaningGUI()">Open GUI</button>
    </div>

    <div id="ScheduleTasks" class="tabcontent">
      <h3>Schedule Tasks</h3>
      <p>Show the schedule tasks dialog</p>
      <button onclick="showScheduleTasksDialog()">Show Dialog</button>
    </div>

    <div id="ProjectFolders" class="tabcontent">
      <h3>Project Folders</h3>
      <p>Show the project folders dialog</p>
      <button onclick="showProjectFoldersDialog()">Show Dialog</button>
    </div>

    <div id="QuoteTasks" class="tabcontent">
      <h3>Quote Tasks</h3>
      <p>Show the quote tasks dialog</p>
      <button onclick="showQuoteTasksDialog()">Show Dialog</button>
    </div>

    <div id="ConnectIOT" class="tabcontent">
      <h3>Connect IoT Device</h3>
      <p>Connect to the IoT device</p>
      <button onclick="connectToIoTDevice()">Connect</button>
    </div>
'''
# Define the JavaScript functions for the button actions
js = '''
    <script>
        function openDataCleaningGUI() {
            // TODO: Add code to open data cleaning GUI
        }

        function showScheduleTasksDialog() {
            // TODO: Add code to show schedule tasks dialog
        }

        function showProjectFoldersDialog() {
            // TODO: Add code to show project folders dialog
        }

        function showQuoteTasksDialog() {
            // TODO: Add code to show quote tasks dialog
        }

        function connectToIoTDevice() {
            // TODO: Add code to connect to IoT device
        }
    </script>
'''

# Add the JavaScript functions to the Streamlit app
st.components.v1.html(js)

# Add the HTML code to the Streamlit app
st.components.v1.html(html, height=500)

# Define the functions for the button actions
def open_data_cleaning_gui():
    # TODO: Add code to open data cleaning GUI
    pass

def show_schedule_tasks_dialog():
    # TODO: Add code to show schedule tasks dialog
    pass

def show_project_folders_dialog():
    # TODO: Add code to show project folders dialog
    pass

def show_quote_tasks_dialog():
    # TODO: Add code to show quote tasks dialog
    pass

def connect_to_iot_device():
    # TODO: Add code to connect to IoT device
    pass

user_input = st.text_input("Enter your question: ")
if user_input:
    sparky = SparkyAssistantGPT4()
    response = sparky.generate_response(user_input)
    st.write("Sparky: ", response)

