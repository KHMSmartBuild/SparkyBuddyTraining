import csv

def append_data_to_csv(task, input_data, output_data, csv_file='data/raw_data/training_datasets.csv'):
    """
    Append data to a CSV file.

    Args:
        task (str): The task description.
        input_data (str): The input data for the task.
        output_data (str): The expected output for the task.
        csv_file (str, optional): The path to the CSV file. Defaults to 'data/raw_data/training_datasets.csv'.
    """
    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([task, input_data, output_data])

if __name__ == "__main__":
    print("Enter task, input, and output. Type 'quit' to exit.")

    while True:
        task = input("Enter task: ")
        if task.lower() == 'quit':
            break

        input_data = input("Enter input: ")
        if input_data.lower() == 'quit':
            break

        output_data = input("Enter output: ")
        if output_data.lower() == 'quit':
            break

        append_data_to_csv(task, input_data, output_data)
        print("Data added successfully!")
