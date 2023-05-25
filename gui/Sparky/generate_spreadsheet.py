import os
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION_ID")

def read_workspace_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def generate_project_info(workspace_text):
    # Split the text into smaller chunks (e.g., 2000 tokens)
    text_chunks = split_text(workspace_text, 2000)

    organized_info = ""
    for chunk in text_chunks:
        prompt = f"Organize the following project information into a structured format:{chunk}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300,
            n=1,
            stop=None,
            temperature=0.5,
        )
        organized_info += response.choices[0].text.strip()

    return organized_info

def split_text(text, max_tokens):
    words = text.split()
    chunks = []

    current_chunk = []
    current_chunk_length = 0
    for word in words:
        word_length = len(word) + 1  # Add 1 for the space before the word
        if current_chunk_length + word_length > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_chunk_length = 0

        current_chunk.append(word)
        current_chunk_length += word_length

    # Add the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def create_spreadsheet(data, file_name='project_spreadsheet.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    workspace_file = "workspace_structure.txt"
    workspace_text = read_workspace_file(workspace_file)
    organized_info = generate_project_info(workspace_text)

    # You can process the organized_info text into a structured format (e.g., list of dictionaries) before passing it to create_spreadsheet()
    structured_data = [
        {'Task': 'Sample task 1', 'Deadline': '2023-05-15'},
        {'Task': 'Sample task 2', 'Deadline': '2023-06-30'},
        # Add more dictionaries with keys and values for additional rows
    ]


    create_spreadsheet(structured_data)
    print("Spreadsheet created.")
