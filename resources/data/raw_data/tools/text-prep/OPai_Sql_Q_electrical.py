import os
import openai
from gui.Sparky.settings.commands.QuotingCommands import Quoting
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()


# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Retrieve the commands for creating, updating, and getting quotes
quoting = Quoting()


# Define the commands for creating, updating, and getting quotes
def create_quote(client_info, job_details):
    # Generate quote using GPT-4
    prompt = f"Create a quote for client {client_info} with job details: {job_details}"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=100
    )
    generated_quote = response.choices[0].text.strip()
    
    # Save generated quote to the database
    return quoting.create_quote(client_info, generated_quote)

def update_quote(quote_id, updated_info):
    return quoting.update_quote(quote_id, updated_info)

def get_quote(quote_id):
    return quoting.get_quote(quote_id)

# Function to search for electrical knowledge
def search_electrical_knowledge(keywords):
    # Load the embeddings dataframe
    df=pd.read_csv('processed/embeddings.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

    # Combine all the texts into a single string for searching
    combined_text = ". ".join(df['text'].tolist())

    # Create a prompt for the OpenAI API
    prompt = f"Search for information about {', '.join(keywords)} in the field of electrical knowledge:\n\n{combined_text}\n\n"

    # Use the OpenAI API to get an answer to the prompt
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        n=1,
        stop=None
    )

    # Return the generated answer
    return response.choices[0].text.strip()

# Example Usage
if __name__ == "__main__":
    client_info = "John Smith"
    job_details = "Install a new consumer unit in the basement"
    new_quote_id = create_quote(client_info, job_details)
    print(f"Created quote ID: {new_quote_id}")

    updated_info = "Upgrade the consumer unit in the basement and install new wiring"
    update_quote(new_quote_id, updated_info)
    print(f"Updated quote ID: {new_quote_id}")

    quote_data = get_quote(new_quote_id)
    print(f"Quote data: {quote_data}")

    keywords = ["electrical theory", "uk electrician", "bs7671", "iet"]
    search_result = search_electrical_knowledge(keywords)
    print(f"Search result: {search_result}")
