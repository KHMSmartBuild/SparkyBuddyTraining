import sqlite3
import time

import requests
from bs4 import BeautifulSoup


def extract_data_from_thread(thread_url, headers):
    """Extracts the question and best answer from a given thread URL.

    Args:
        thread_url (str): The URL of the thread to extract data from.

    Returns:
        tuple: A tuple containing the question string and best answer string, respectively.
            Returns None if the data could not be extracted.
    """
    response = requests.get(thread_url, headers=headers)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to retrieve thread data from URL: {thread_url}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    
    try:
        question = soup.find("div", {"class": "question"}).text
        best_answer = soup.find("div", {"class": "best-answer"}).text
    except AttributeError:
        print(f"Failed to extract data from thread: {thread_url}")
        return None

    return question, best_answer


if __name__ == "__main__":
    base_url = "https://www.electriciansforums.net/forums/electrical-wiring-theories-and-regulations.9/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    

    # Open a connection to the database
    conn = sqlite3.connect('electrician_forum.db')

    # Create a cursor object
    c = conn.cursor()

    # Execute a query
    query = "SELECT * FROM threads"
    c.execute(query)

    # Fetch the results
    results = c.fetchall()

    # Print the results to the console
    print(results)

    # Close the cursor and the connection
    c.close()
    conn.close()
    # Create an SQLite database and table to store the data
    with sqlite3.connect("electrician_forum.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS threads (question TEXT, best_answer TEXT)")

        # Loop through each page of threads and extract the question and best answer for each thread
        for page in range(1, 12):
            page_url = base_url + f"page-{page}"
            response = requests.get(page_url, headers=headers)

            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Failed to retrieve page data from URL: {page_url}")
                continue

            time.sleep(1)

            soup = BeautifulSoup(response.content, "html.parser")
            thread_links = soup.find_all("a", {"class": "thread-link"})

            for thread_link in thread_links:
                thread_url = thread_link["href"]
                data = extract_data_from_thread(thread_url, headers)

                if data:
                    question, best_answer = data
                    c.execute("INSERT INTO threads VALUES (?, ?)", (question, best_answer))
                    print(f"Inserted data into threads table: {question}")
