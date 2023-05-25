# Script Name: train_sparky.py
# Location: Sparky  training/gui/Sparky/train_sparky.py
# Author: KHM Smartbuild
# Purpose: TODO add this purpose
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild


# Import necessary libraries
import os
import random
import json

current_dir = os.path.dirname(os.path.abspath(__file__))

# Load Sparky's personality from JSON file
with open(os.path.join(current_dir, "sparky_personality.json"), "r") as file:
    sparky_personality = json.load(file)
    
# Extract Sparky's core traits, behavior, and mannerisms from the JSON data
core_traits = sparky_personality['core_traits']
behavior = sparky_personality['behavior']
mannerisms = sparky_personality['mannerisms']

# Create a prompt incorporating Sparky's personality traits
prompt = f"With a personality that includes the following core traits: {core_traits}, behavior: {behavior}, and mannerisms: {mannerisms}, you are Sparky's training model. You will help me with training Sparky's model."


# Define Sparky Buddy 3's greeting
def greet():
    greeting = random.choice(list(sparky_personality["mannerisms"]["regional_accent_examples"].values()))
    return greeting


# Define Sparky Buddy 3's response to connecting with devices
def device_connected():
    response = sparky_personality["mannerisms"]["connection_with_devices_anecdote"]
    return response

# Define Sparky Buddy 3's response to discussing hobbies
def hobby_hint(topic=None):
    hint = None
    if topic and topic in sparky_personality["hobbies"]["hobby_references"]["situations"]:
        hint = random.choice(["Oh, that reminds me of my own interest in {}.", "I'm always looking for ways to incorporate {} into my work.", "Have you considered how {} could benefit your electrical projects?"]).format(topic)
    return hint


# Define Sparky Buddy 3's joke
def tell_joke():
    joke = "Why did the electrician go to art school? To learn how to wire a frame!"
    return joke

# Define Sparky Buddy 3's response to illegal or unsafe practices
def explain_implications():
    explanation = "I'm sorry, but engaging in illegal or unsafe practices could result in serious harm or legal consequences. Let's find a safer and more ethical solution."
    return explanation

# Define function to get Sparky Buddy 3's entire personality
def get_sparky_personality():
    return sparky_personality