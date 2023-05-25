import os

def save_data(processed_data, output_dir, filename):
    """
    Saves preprocessed data to a file.

    Args:
        processed_data (str): Preprocessed data to be saved.
        output_dir (str): Directory path where the file should be saved.
        filename (str): Name of the file to be saved.

    Returns:
        None
    """

    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # create the directory if it does not exist

    # Save the preprocessed data to a file
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as file:
        file.write(processed_data)  # write the processed data to the file