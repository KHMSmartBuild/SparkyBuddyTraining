import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

def remove_stopwords(text):
    """
    Remove stopwords from the given text.

    Args:
    - text: A string containing the text to process.

    Returns:
    - A string with stopwords removed.
    """
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text)
    filtered_text = [word for word in tokens if word.lower() not in stop_words]
    return ' '.join(filtered_text)

def lemmatize_text(text):
    """
    Lemmatize the given text.

    Args:
    - text: A string containing the text to process.

    Returns:
    - A string with lemmatized words.
    """
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    lemmatized_text = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(lemmatized_text)

def remove_punctuation(text):
    """
    Remove punctuation from the given text.
    
    Args:
    - text: A string containing the text to process.

    Returns:
    - A string with punctuation removed.
    """
    text = re.sub(r'[^\w\s]', '', text)
    return text

def remove_numbers(text):
    """
    Remove numbers from the given text.
    
    Args:
    - text: A string containing the text to process.

    Returns:
    - A string with numbers removed.
    """
    text = re.sub(r'\d+', '', text)
    return text

def to_lower(text):
    """
    Convert the given text to lowercase.
    
    Args:
    - text: A string containing the text to process.

    Returns:
    - A string in lowercase.
    """
    return text.lower()

def preprocess_text(text, remove_punct=True, remove_num=True, to_lowercase=True):
    """
    Apply preprocessing steps to the given text based on the function arguments.
    
    Args:
    - text: A string containing the text to process.
    - remove_punct: A boolean indicating whether to remove punctuation.
    - remove_num: A boolean indicating whether to remove numbers.
    - to_lowercase: A boolean indicating whether to convert text to lowercase.

    Returns:
    - A preprocessed string based on the given options.
    """
    if remove_punct:
        text = remove_punctuation(text)
    if remove_num:
        text = remove_numbers(text)
    if to_lowercase:
        text = to_lower(text)
    return text

def preprocess_data(raw_data):
    """
    Preprocess the raw data by applying the default preprocessing steps.
    
    Args:
    - raw_data: A string containing the raw data to process.

    Returns:
    - A preprocessed string.
    """
    preprocessed_data = preprocess_text(raw_data)
    return preprocessed_data
