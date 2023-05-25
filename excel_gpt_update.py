import os
import re
import csv
import openai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import logging

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a function to use NLP to analyze the file names and descriptions
def analyze_text(text):
    # Use the GPT-3 language model to analyze the text
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Analyze the following text:\n{text}\n\nIdentify any patterns or inconsistencies in the text.",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the analyzed text from the OpenAI response
    analyzed_text = response.choices[0].text.strip()

    # Return the analyzed text
    return analyzed_text

# Define a function to check the gathered information
def check_info(file_info):
    # Extract the name and description from the file info
    name = file_info['Name']
    description = file_info['Description']

    # Analyze the name and description using NLP
    analyzed_name = analyze_text(name)
    analyzed_description = analyze_text(description)

    # Check if the analyzed name and description match the original name and description
    if name != analyzed_name or description != analyzed_description:
        # If the analyzed name or description is different, print a warning message
        print(f"Warning: Possible error or inconsistency found in the following file:\nName: {name}\nDescription: {description}")
        print(f"Analyzed Name: {analyzed_name}\nAnalyzed Description: {analyzed_description}")
    else:
        # If the analyzed name and description match the original name and description, print a success message
        print(f"Success: The following file has been verified:\nName: {name}\nDescription: {description}")

    # Call the check_info function for each file in the project
    for file_info in project_files:
        check_info(file_info)

# Define the path to the project folder
path = "/path/to/project/folder"

# Define the columns for the CSV file
columns = ["Name", "Description", "Dependencies/Requirements", "Script Type",
           "Module", "Classes", "Functions", "Variables", "Strings",
           "Relationships to Other Scripts", "Notes", "Checklist"]

# Define the regular expression for file extensions
ext_regex = r"\.(js|py|java|c|cpp|cs|php|rb|go)$"

# Create an empty list to store the data for each file
data = []

# Loop through all the files in the project folder
for root, dirs, files in os.walk(path):
    for file in files:
        # Check if the file has a valid extension
        if re.search(ext_regex, file):
            # Initialize the data for this file
            file_data = {"Name": file,
                         "Description": "",
                         "Dependencies/Requirements": "",
                         "Script Type": "",
                         "Module": "",
                         "Classes": "",
                         "Functions": "",
                         "Variables": "",
                         "Strings": "",
                         "Relationships to Other Scripts": "",
                         "Notes": "",
                         "Checklist": ""}

            # Read the contents of the file
            with open(os.path.join(root, file), "r") as f:
                contents = f.read()

            # Analyze the contents of the file and update the file data
            # (insert your analysis code here)

            # Append the file data to the list of data
            data.append(file_data)

# Write the data to a CSV file
with open("project_data.csv", "w") as f:
    # Write the header row
    f.write(",".join(columns) + "\n")

    # Write the data rows
    for file_data in data:
        row = [file_data[column] for column in columns]
        f.write(",".join(row) + "\n")

print("Project data saved to project_data.csv")