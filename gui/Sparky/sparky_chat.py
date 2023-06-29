# Script name : sparky_chat.py
# location = gui\Sparky\sparky_chat.py
# accessable from Libraries = yes
# Author: KHM Smartbuild
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild. All rights reserved.

import sys
import os
import json
import openai
from datetime import datetime
from dotenv import load_dotenv
from gui.Sparky.train_sparky import prompt, greet, device_connected, hobby_hint, explain_implications, sparky_personality
from gui.Sparky.sparky_features import  Sparky_InventoryControl, Sparky_Payroll,Sparky_ElectricalTheory,Sparky_IoTConnection,Sparky_CustomerCare,Sparky_JobScheduling,Sparky_quoting
from gui.utils.database.history import create_connection, save_conversation_log, get_conversation_history, save_conversation_history, load_conversation_history, check_if_table_exists

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

        # Define the functions that the chat model can call
        functions = [
            {
                "name": "Sparky_quoting",
                "description": "Generate a quote based on client information and job details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "client_info": {"type": "string"},
                        "job_details": {"type": "string"}
                    },
                    "required": ["client_info", "job_details"]
                }
            }
            # Add more function definitions here as needed
        ]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613 ",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=1500,
                n=1,
                stop=["\n"],
                temperature=self.temperature,
                functions=functions  # Add the functions parameter here
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
            device_connected: ["device connected"],
            explain_implications: ["explain the implications"],
            hobby_hint: ["give me a hint about"],
            Sparky_quoting: ["give me a quote", "quote"],
            Sparky_InventoryControl: ["inventory check", "stock check", "inventory query"],
            Sparky_Payroll: ["payroll query", "payroll"],
            Sparky_JobScheduling: ["schedule job", "job scheduling"],
            Sparky_CustomerCare: ["customer support", "support"],
            Sparky_IoTConnection: ["iot query", "smart home", "connected home"],
            Sparky_ElectricalTheory: ["electrical query", "electrical theory"],
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






