import random

def split_data(text, train_ratio=0.9):
    """
    Splits the text into train and validation sets.

    Args:
        text (str): The input text to be split.
        train_ratio (float): The ratio of the text to be assigned to the training set.

    Returns:
        tuple: A tuple containing the train and validation sets as strings.
    """
    lines = text.split("\n")
    shuffled_lines = lines.copy()   # make a copy of the lines list
    random.shuffle(shuffled_lines)
    num_train = int(train_ratio * len(shuffled_lines))
    train_lines = shuffled_lines[:num_train]
    val_lines = shuffled_lines[num_train:]
    return "\n".join(train_lines), "\n".join(val_lines)

def save_to_file(filename, content):
    """
    Saves the given content to a file.

    Args:
        filename (str): The path of the file to save the content.
        content (str): The content to be saved.
    """
    with open(filename, "w") as f:
        f.write(content)

def main(input_file, train_output_file, val_output_file):
    """
    Main function to load cleaned text, split it into train and validation sets, and save them to separate files.

    Args:
        input_file (str): The path of the cleaned text file.
        train_output_file (str): The path of the output file for the train set.
        val_output_file (str): The path of the output file for the validation set.
    """
    # Load the cleaned text from the file
    with open(input_file, "r") as f:
        cleaned_text = f.read()

    # Split the data into train and validation sets
    train_text, val_text = split_data(cleaned_text)

    # Save the train and validation sets to separate files
    save_to_file(train_output_file, train_text)
    save_to_file(val_output_file, val_text)

# Example usage:
input_file = "data/processed_data/cleaned_text.txt"
train_output_file = "train.txt"
val_output_file = "val.txt"
main(input_file, train_output_file, val_output_file)