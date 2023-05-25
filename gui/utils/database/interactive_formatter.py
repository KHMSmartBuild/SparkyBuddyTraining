# Script name : interactive_formatter.py
#Location = gui\utils\prep\interactive_formatter.py
# Author: KHM Smartbuild
# Purpose: 
"""
This script is used to format the output of the GUI.

"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import sqlite3

DATABASE_FILE = 'BS7671_database.db'

def create_connection():
    """Create a database connection to a SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
    except sqlite3.Error as e:
        print(e)
    return conn

def get_random_question():
    """
    Retrieves a random question from the database along with its section title and answers.

    Returns:
    A tuple containing the randomly selected question text, section title, and a list of answer texts. If no question is found, returns None.
    """
    conn = create_connection()
    if not conn:
      return None
    c = conn.cursor()
    c.execute('SELECT question_text, section_title FROM Questions INNER JOIN Sections ON Questions.section_id = Sections.section_id ORDER BY RANDOM() LIMIT 1')
    result = c.fetchone()
    if not result:
      return None
    question, section = result
    c.execute('SELECT answer_text FROM Answers WHERE question_id = (SELECT question_id FROM Questions WHERE question_text = ?)', (question,))
    answers = [row[0] for row in c.fetchall()]
    conn.close()
    return question, section, answers

def display_question(question, section, answers):
    """
    Display a question along with its section and possible answers.

    Args:
    - question (str): The text of the question to be displayed.
    - section (str): The section of the question.
    - answers (list): A list of strings representing possible answers to the question.

    Returns:
    - None: This function doesn't return anything, it just prints the question and answers.
    """
    print(f"Section: {section}")
    print(f"Question: {question}")
    for i, answer in enumerate(answers):
        print(f"{i+1}. {answer}")

def prompt_user_answer():
    """
    Prompts the user for an answer and returns the input as a string.
    :return: a string representing the user's answer
    """  
    return input("Your answer: ")

def compare_user_answer(user_answer, correct_answers):
    """
    Checks if the user's answer matches any of the correct answers provided. 

    :param user_answer: A string representing the user's answer
    :type user_answer: str
    :param correct_answers: A list of strings representing the correct answers
    :type correct_answers: list[str]
    :return: A boolean value indicating whether the user's answer matches any of the correct answers provided
    :rtype: bool
    """
    return user_answer.lower() in [a.lower() for a in correct_answers]

def provide_feedback(correct, explanation):
    """
    Provide feedback on whether an answer is correct or not and explain the solution.

    :param correct: A boolean indicating whether the answer is correct or not.
    :type correct: bool
    :param explanation: A string explaining the solution to the problem.
    :type explanation: str
    :return: None
    """
    if correct:
        print("Correct!")
    else:
        print("Incorrect.")
    print(explanation)

def main():
    """
    Runs a loop that prompts the user to press enter to get a new question or enter 'q' to quit.
    If 'q' is not entered, a random question is selected from the database and displayed to the user.
    The user's answer is compared to the correct answer and feedback is provided.
    """
    while True:
        try:
            input("Press enter to get a new question or 'q' to quit...")
        except KeyboardInterrupt:
            break
        question_data = get_random_question()
        if question_data is None:
            print("Error: No questions found in database.")
        else:
            question, section, answers = question_data
            display_question(question, section, answers)
            user_answer = prompt_user_answer()
            correct = compare_user_answer(user_answer, answers)
            provide_feedback(correct, "The correct answer is: " + ", ".join(answers))

if __name__ == '__main__':
    main()
