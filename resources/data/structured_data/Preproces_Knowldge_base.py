from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sqlite3
import os
import re
import logging

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s %(message)s')


# Load the pre-trained model and tokenizer
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Define a function to extract key information from text using the pre-trained model
"""
Extracts key information from the given text using a pre-trained transformer model.
:param text: The text to extract key information from.
:type text: str
:return: The label for the key information extracted from the text.
:rtype: int
"""

def extract_key_information(text):
    try:
        # Truncate the text to fit within the model's max length
        text = text[:tokenizer.model_max_length-2]

        # Tokenize the input text and convert to PyTorch tensor
        inputs = tokenizer(text, return_tensors="pt", truncation=True)
        # Pass the tensor through the model and get the classification scores
        outputs = model(**inputs)
        # Apply softmax to the scores to get probabilities for each label
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        # Get the label with highest probability
        label = torch.argmax(probabilities)
        # Return the label as an integer
        return label.item() if label is not None else None
    except Exception as e:
        logging.error(f"Error extracting key information: {e}")
        return None

# Define the path to the SQLite database
database_path = "databases/knowledge_base.db"

# Check if the database file exists
if not os.path.isfile(database_path):
    raise FileNotFoundError("Cannot find database file")

# Connect to the database and create a cursor object
with sqlite3.connect(database_path) as conn:
    cursor = conn.cursor()

    # Define the output file path
    output_file = 'fine_tuning_data.txt'

    # Define a function to preprocess the content
    """
Preprocesses a given string by removing all non-alphanumeric characters and converting all characters to lowercase.

:param content: The string to preprocess.
:type content: str
:return: The preprocessed string.
:rtype: str
"""

    def preprocess_content(content):
        # Remove all non-alphanumeric characters and convert all characters to lowercase
        content = re.sub(r'[^\w\s]', '', content).lower()
        # Return the preprocessed string
        return content


    # Define a function to get the list of tables in the database
    """
Return a list of all table names in the SQLite database.

Args:
    cursor: A cursor object for the SQLite database.

Returns:
    A list of strings representing all table names in the database.
"""

    def get_tables(cursor):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [table[0] for table in cursor.fetchall()]

    def get_column_names(cursor, table_name):
        cursor.execute(f"PRAGMA table_info({table_name})")
        return [col[1] for col in cursor.fetchall()]

    # Open the output file in 'append' mode to add to existing data
    with open(output_file, 'a') as f:
        # Add a comment line to clarify output format
        f.write("# label\tcontent\n")

        # Loop through each table in the database
        for table_name in get_tables(cursor):
            column_names = get_column_names(cursor, table_name)
            # Replace 'id' and 'content' with the correct column names in your tables
            id_col, content_col = column_names[0], column_names[1]
            cursor.execute(f"SELECT {id_col}, {content_col} FROM {table_name}")

        # Loop through each row in the result set
        for row in cursor.fetchall():
        # Extract the page number and content from the row
            page_num, content = row
        # Check if the content is not empty
        if content:
            # Preprocess the content and extract the label using the pre-trained model
            preprocessed_content = preprocess_content(content)
            label = extract_key_information(preprocessed_content)
        if label is not None:
            # Open the output file in 'append' mode to add to existing data
            with open(output_file, 'a') as f:
                # Write the label and preprocessed content to the output file
                f.write(f"{label}\t{preprocessed_content}\n")
        else:
            logging.error(f"Failed to extract key information for row {row}")



    # Print a message to indicate that the writing is complete
    print(f"Done writing to file {output_file}")
