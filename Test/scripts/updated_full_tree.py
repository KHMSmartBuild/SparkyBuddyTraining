import os

def list_files(startpath, exclude_dirs=None):
    if exclude_dirs is None:
        exclude_dirs = []

    files_list = []

    for root, dirs, files in os.walk(startpath):
        # Exclude the directories you don't want to include
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        files_list.append('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)
        for f in files:
            files_list.append('{}{}'.format(subindent, f))

    return files_list

def get_functions(source):
    namespace = {}
    exec(source, namespace)
    
    functions = []
    for name, obj in inspect.getmembers(namespace):
        if inspect.isfunction(obj):
            functions.append(name)

    return functions

output_file = 'output.txt'
startpath = '.'  # Change this to the desired starting directory
exclude_dirs = ['venv']  # Add any other directories you want to exclude

file_list = list_files(startpath, exclude_dirs)

with open(output_file, "w") as f:
    for file in file_list:
        f.write(file + '\n')

import os
import csv
import openai
from dotenv import load_dotenv

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

# define the columns for the output CSV
fields = ['Name', 'Description', 'Dependencies/Requirements', 'Script Type', 'Module', 'Classes', 'Functions', 'Variables', 'Strings', 'Relationships to Other Scripts', 'Notes', 'Checklist']

# create an empty dictionary to hold the script information
script_info = {}

# iterate over all the Python files in the directory using a generator expression
for filename in (f for f in os.listdir('.') if f.endswith('.py')):
    # get the name of the script
    name = os.path.splitext(filename)[0]

    # open the script file and read the contents
    with open(filename, 'r') as f:
        contents = f.read()

    # extract information about the script and add it to the dictionary
    # replace these lines with your own code to extract the desired information
    description = 'TODO'
    dependencies = 'TODO'
    script_type = 'TODO'
    module = 'TODO'
    classes = 'TODO'
    functions = 'TODO'
    variables = 'TODO'
    strings = 'TODO'
    relationships = 'TODO'
    notes = 'TODO'
    checklist = 'TODO'
    script_info[name] = {
        
    }
