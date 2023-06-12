# Import necessary modules
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import logging
import sys

def setup_logging():
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format, handlers=[logging.StreamHandler(sys.stdout)])

# Download necessary data for the nltk module
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("stopwords")

def clean_and_tokenize(text):
    """
    Clean and tokenize a given text.

    Args:
        text (str): The input text to be cleaned and tokenized.

    Returns:
        list: A list of cleaned and tokenized words.
    """
    # Remove punctuation from the text
    text = remove_punctuation(text)
    # Tokenize the text into individual words
    words = tokenize(text)
    # Remove stop words from the list of words
    words = remove_stop_words(words)
    # Lemmatize the list of words
    words = lemmatize(words)

    return words

def remove_punctuation(text):
    """
    Remove all punctuation characters from the input text.

    Args:
        text (str): A string containing punctuation characters.

    Returns:
        str: The input text with all punctuation characters removed.
    """
    return text.translate(str.maketrans("", "", string.punctuation))

def tokenize(text):
    """
    Tokenizes the given text into individual words.

    Args:
        text (str): The text to be tokenized.

    Returns:
        list[str]: A list of words in the text.
    """
    return nltk.word_tokenize(text.lower())

def remove_stop_words(words):
    """
    Remove stop words from a list of words.

    Args:
        words (list[str]): A list of words.

    Returns:
        list[str]: A new list of words with stop words removed.
    """
    return [word for word in words if word not in stopwords.words("english")]

def lemmatize(words):
    """
    Lemmatizes a list of words using WordNetLemmatizer.

    Args:
        words (list[str]): A list of words to lemmatize.

    Returns:
        list[str]: A list of the lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word) for word in words]

def process_text(input_path, output_path):
    """
    Process the text in the input file and write the cleaned text to the output file.

    Args:
        input_path (str): A string representing the path to the input file.
        output_path (str): A string representing the path to the output file.

    Returns:
        None
    """
    try:
        with open(input_path, 'r', encoding='utf-8') as input_file:
            # Read the raw text from the input file
            raw_text = input_file.read()
            # Clean and tokenize the raw text
            cleaned_text = clean_and_tokenize(raw_text)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                # Write the cleaned text to the output file
                output_file.write(' '.join(cleaned_text))
    except FileNotFoundError:
        print(f"Input file not found: {input_path}. Skipping processing.")

def main(input_file, output_file):
    setup_logging()
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")
    process_text(input_file, output_file)

if __name__ == "__main__":
    input_file = input("Enter the input file path: ")
    output_file = input("Enter the output file path: ")
    main(input_file, output_file)
