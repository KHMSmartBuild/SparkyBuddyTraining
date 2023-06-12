import requests
from bs4 import BeautifulSoup
import sqlite3

# Define the URL of the electrician forum page you want to scrape
url = "https://www.electriciansforums.net/forums/electrical-wiring-theories-and-regulations.9/"

# Send a GET request to the page and get the response
response = requests.get(url)

# Create a Beautiful Soup object from the HTML content of the response
soup = BeautifulSoup(response.content, "html.parser")

# Find all links to individual threads on the page
thread_links = soup.find_all("a", {"class": "thread-link"})

# Define the function to extract the question and best answer from a thread
def extract_data_from_thread(thread_url):
    # Send a GET request to the thread page and get the response
    response = requests.get(thread_url)

    # Create a Beautiful Soup object from the HTML content of the response
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the question and best answer from the thread
    question = soup.find("div", {"class": "question"}).text
    best_answer = soup.find("div", {"class": "best-answer"}).text

    # Return a tuple containing the question and best answer
    return (question, best_answer)

# Create an SQLite database and table to store the data
conn = sqlite3.connect("electrician_forum.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS threads (question TEXT, best_answer TEXT)")

# Loop through each thread and extract the question and best answer
for thread_link in thread_links:
    thread_url = thread_link["href"]
    question, best_answer = extract_data_from_thread(thread_url)

    # Insert the data into the SQLite database
    c.execute("INSERT INTO threads VALUES (?, ?)", (question, best_answer))

    # Insert the data into the SQLite database
    c.execute("INSERT INTO threads VALUES (?, ?)", (question, best_answer))
    print(f"Inserted data into database: {question}, {best_answer}")
    
# Commit the changes and close the database connection
conn.commit()
conn.close()