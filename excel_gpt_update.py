import os
import re
import csv
import openai
from dotenv import load_dotenv
import pandas as pd
import numpy as np
import logging
from multiprocessing import Pool

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Use the GPT-3 language model to analyze the file contents
def analyze_file(file_path):
    # Read the contents of the file
    with open(file_path, "r") as f:
        contents = f.read()

    # Use the GPT-3 language model to analyze the contents
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Analyze the following text:\n{contents}\n\nIdentify any patterns or inconsistencies in the text.",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the analyzed text from the OpenAI response
    analyzed_text = response.choices[0].text.strip()

    # Check if the analyzed text is in the expected format
    if "\n\n" in analyzed_text:
        # If the analyzed text is in the expected format, split it into name and description
        analyzed_name, analyzed_description = analyzed_text.split("\n\n", 1)
    else:
        # If the analyzed text is not in the expected format, set the name and description to empty strings
        analyzed_name, analyzed_description = "", ""

    # Return the analyzed text
    return analyzed_name, analyzed_description

    # ...



def check_info(file_data):
    name = file_data['Name']
    description = file_data['Description']
    analyzed_name = file_data['Analyzed Name']
    analyzed_description = file_data['Analyzed Description']

    if name != analyzed_name or description != analyzed_description:
        print(f"Warning: Possible error or inconsistency found in the following file:\nName: {name}\nDescription: {description}")
        print(f"Analyzed Name: {analyzed_name}\nAnalyzed Description: {analyzed_description}")
    else:
        print(f"Success: The following file has been verified:\nName: {name}\nDescription: {description}")

def main():
    path = ""
    columns = ["Name", "Description", "Dependencies/Requirements", "Script Type",
               "Module", "Classes", "Functions", "Variables", "Strings",
               "Relationships to Other Scripts", "Notes", "Checklist", "Analyzed Name", "Analyzed Description"]
    ext_regex = r"\.(js|py|java|c|cpp|cs|php|rb|go)$"
    data = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if re.search(ext_regex, file):
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
                             "Checklist": "",
                             "Analyzed Name": "",
                             "Analyzed Description": ""}

                # Analyze the contents of the file using NLP in a separate process
                file_path = os.path.join(root, file)
                with Pool(processes=1) as pool:
                    analyzed_text = pool.apply_async(analyze_file, (file_path,))
                    analyzed_name, analyzed_description = analyzed_text.get()

                # Update the file data with the analyzed text
                file_data['Analyzed Name'] = analyzed_name
                file_data['Analyzed Description'] = analyzed_description

                data.append(file_data)

    for file_data in data:
        check_info(file_data)

    with open("project_data.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

    print("Project data saved to project_data.csv")

if __name__ == "__main__":
    main()
