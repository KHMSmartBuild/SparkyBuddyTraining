# Script name : sparky_chat.py
# location = gui\Sparky\sparky_chat.py
# accessable from Libraries = yes
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild
# Purpose:
"""_summary_
This script is named sparky_chat.py and is located at gui\Sparky\sparky_chat.py. It is accessible from the Libraries. The script creates a chatbot named Sparky, designed to help electricians in the UK, using OpenAI's GPT-3 API.

The script imports various modules, loads environment variables, sets up logging, and defines a SparkyChat class with methods for generating chatbot responses based on user input. The SparkyChat class also includes methods to manage the chatbot's personality and generate its description.

The generate_chat_response function handles various user inputs using a keyword map and calls the appropriate function. It then generates a response and saves the conversation log in a SQLite database.

 _Functions_
The script imports and uses the following functions from Sparky and Sparky.history:

prompt
greet
device_connected
hobby_hint
tell_joke
explain_implications
sparky_personality
create_connection
save_conversation_log
get_conversation_history
save_conversation_history
load_conversation_history
check_if_table_exists
The script also configures logging with various log levels to keep track of the chatbot's operation.
Returns:
    _type_: _description_
"""

import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
Sparky_dir = os.path.join(parent_dir, 'Sparky')
utils_dir = os.path.join(parent_dir, 'utils')
sys.path.insert(0, utils_dir)

import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from train_sparky import prompt, greet, device_connected, hobby_hint, tell_joke, explain_implications, sparky_personality
from sparky_features import Quoting, InventoryControl, Payroll, JobScheduling, CustomerCare, IoTConnection, ElectricalTheory
from utils.database.history import create_connection, save_conversation_log, get_conversation_history, save_conversation_history, load_conversation_history, check_if_table_exists

import logging
import sqlite3 
logging.basicConfig(filename='sparky_chat.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

# Use logger in your code
logging.debug('Debug message')
logging.info('Informational message')
logging.warning('Warning message')
logging.error('Error message')
logging.critical('Critical message')

load_dotenv()

class SparkyChat:
    """
A class for creating and managing a Sparky chatbot using OpenAI's GPT-3 API.

Attributes
----------
api_key : str
    The OpenAI API key used to authenticate API requests.
temperature : float
    The temperature setting used when generating chatbot responses.
use_azure : bool
    A flag indicating whether to use Microsoft Azure as a fallback for API requests.
sparky_personality : dict
    A dictionary containing various personality traits and characteristics for the Sparky chatbot.

Methods
-------
get_personality_description(personality: dict) -> str:
    Returns a string description of the given personality dictionary.

generate_response(user_input: str) -> str:
    Generates a chatbot response using OpenAI's GPT-3 API based on the given user input.

"""
    
    def __init__(self):
        """
    Initializes a new instance of the SparkyChat class.

    Raises
    ------
    FileNotFoundError
        If the "sparky_personality.json" file cannot be found in the same directory as this script.

    """

        self.api_key = os.getenv("OPENAI_API_KEY")
        self.organization = os.getenv("OpenAI_organization")
        self.temperature = float(os.getenv("TEMPERATURE", 0))
        self.use_azure = os.getenv("USE_AZURE", "False").lower() == "true"

        current_dir = os.path.dirname(os.path.abspath(__file__))
        sparky_personality_path = os.path.join(current_dir, "sparky_personality.json")

        with open(sparky_personality_path, "r") as file:
            self.sparky_personality = json.load(file)
            
    def get_personality_description(self, personality):
        """
    Returns a string description of the given personality dictionary.

    Parameters
    ----------
    personality : dict
        A dictionary containing various personality traits and characteristics for the Sparky chatbot.

    Returns
    -------
    str
        A string description of the given personality.

    """
        description = "Sparky has the following personality traits: "
        traits = ', '.join(personality["core_traits"])
        description += traits + ". "
        description += "Sparky's behavior is " + ', '.join(personality["behavior"]) + ". "

        # Mannerisms
        description += "Sparky has the following mannerisms: "
        description += personality["mannerisms"]["regional_accent_examples"]["London"] + " "
        description += personality["mannerisms"]["connection_with_devices_anecdote"] + " "

        # Motivation
        description += "Sparky's primary motivation is to " + personality["motivation"]["primary_motivation"] + ". "
        description += "Sparky's problem-solving approach is to " + personality["motivation"]["problem_solving_approach"] + ". "
        description += "In situations involving " + ', '.join(personality["motivation"]["adaptation"]["situations"]) + ", "
        description += "Sparky will " + personality["motivation"]["adaptation"]["response"] + ". "

        # Humor
        description += "Sparky's humor is " + personality["humor"]["type"] + ". "
        description += "Sparky is " + personality["humor"]["self-awareness"] + ". "
        description += "Sparky is " + personality["humor"]["playful_attraction_to_electrical_equipment"] + ". "

        # Hobbies
        description += "Sparky's interests include " + ', '.join(personality["hobbies"]["interests"]) + ". "
        description += "When discussing environmental impact, relaxation, or planning green energy solutions, "
        description += "Sparky will give subtle hints related to their hobbies."

        return description

    # Define a function to generate a response using OpenAI API
    def generate_response(self, user_input):
        """
        Generates a chatbot response using OpenAI's GPT-3 API based on the given user input.

        Parameters
        ----------
        user_input : str
            The input text from the user.

        Returns
        -------
        str
            A response generated by the chatbot.

        """
        openai.api_key = self.api_key
        
        sparky_description = self.get_personality_description(self.sparky_personality)
        system_message = f"You are a helpful AI for electricians in the UK named Sparky. You are trained specifically in BS7671, best practice guides, guidance note books, and other resources related to UK electrical standards. {sparky_description}"
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_input},
        ],
            max_tokens=1500,
            n=1,
            stop=["\n"],
            temperature=self.temperature,
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                prompt=response.choices[0].text,
                temperature=self.temperature
            )
        except openai.errors.OpenAIError as e:
                logging.error(f"OpenAI API error: {e}")
                return "I'm sorry, I'm having trouble generating a response. Please try again later."

        return response.choices[0].message['content'].strip()

    def generate_chat_response(self, user_input):
        user_input_lower = user_input.lower()
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "databases/conversation_history.db")

        keyword_map = {
            greet: ["hello", "hi", "hey"],
            tell_joke: ["tell me a joke"],
            device_connected: ["device connected"],
            explain_implications: ["explain the implications"],
            hobby_hint: ["give me a hint about"],
            Quoting.generate_quote: ["give me a quote", "quote"],
            InventoryControl.inventory_query: ["inventory check", "stock check", "inventory query"],
            Payroll.payroll_query: ["payroll query", "payroll"],
            JobScheduling.schedule_job: ["schedule job", "job scheduling"],
            CustomerCare.customer_support: ["customer support", "support"],
            IoTConnection.iot_query: ["iot query", "smart home", "connected home"],
            ElectricalTheory.electrical_query: ["electrical query", "electrical theory"],
        }

        try:
            conn = create_connection(db_path)
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")
            return "I'm sorry, I'm having trouble saving the conversation. Please try again later."
        
        for func, keywords in keyword_map.items():
            if any(keyword in user_input_lower for keyword in keywords):
                response = func(self)
                break
        else:
            response = self.generate_response(user_input)

        logging.info(f"Saving conversation log in the database: {db_path}")
        logging.info(f"Table 'conversation_history' exists: {check_if_table_exists(conn, 'conversation_history')}")
        log = (user_input, response, datetime.now())
        save_conversation_log(conn, log)
        logging.info("Conversation log saved.")
        conn.close()

        return response






