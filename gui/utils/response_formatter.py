# Script name : response_formatter.py
#Location = gui\utils\prep\response_formatter.py
# Author: KHM Smartbuild
# Purpose: TODO add purpose of this Script
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild



import os
import re
from typing import List, Tuple
import PIL.Image
from IPython.display import display, Markdown, Image
import base64

import sqlite3


def format_openai_response(response):
    """Format the response from OpenAI's GPT-3 API in a user-friendly way."""
    message = response.choices[0].text.strip()
    formatted_response = f"**Sparky Buddy says:** {message}"
    return formatted_response


def format_definition(definition):
    """Format a definition retrieved from the Definitions table in a user-friendly way."""
    term, definition_text = definition
    formatted_definition = f"**{term}:** {definition_text}"
    return formatted_definition


def format_example(example):
    """Format an example retrieved from the Examples table in a user-friendly way."""
    example_text, _ = example
    formatted_example = f"- {example_text}"
    return formatted_example


def format_image(image_path):
    """Format an image retrieved from the Images table in a user-friendly way."""
    with open(image_path, "rb") as f:
        image = PIL.Image.open(f)
        encoded_image = base64.b64encode(f.read()).decode("utf-8")
        img_tag = f'<img src="data:image/png;base64,{encoded_image}"/>'
    formatted_image = f"\n{img_tag}\n"
    return formatted_image


def format_paragraph(paragraph):
    """Format a paragraph retrieved from the Paragraphs table in a user-friendly way."""
    paragraph_text, _ = paragraph
    formatted_paragraph = f"{paragraph_text}\n"
    return formatted_paragraph


def format_question(question):
    """Format a question retrieved from the Questions table in a user-friendly way."""
    question_text, section_id = question
    formatted_question = f"\n**{question_text}**\n\n"
    return formatted_question, section_id


def format_answer(answer):
    """Format an answer retrieved from the Answers table in a user-friendly way."""
    answer_text, _ = answer
    formatted_answer = f"- {answer_text}\n"
    return formatted_answer


def format_section(section):
    """Format a section retrieved from the Sections table in a user-friendly way."""
    section_title, chapter_id = section
    formatted_section = f"## {section_title}\n"
    return formatted_section, chapter_id


def format_chapter(chapter):
    """Format a chapter retrieved from the Chapters table in a user-friendly way."""
    chapter_title, _ = chapter
    formatted_chapter = f"# {chapter_title}\n"
    return formatted_chapter


def get_database_connection():
    """Create a database connection to a SQLite database."""
    database_file = "knowledge_base.db"
    conn = None
    try:
        conn = sqlite3.connect(database_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def get_random_question():
    """Retrieve a random question from the Questions table in the database, along with its corresponding section and answers."""
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT question_text, section_id, question_id FROM Questions ORDER BY RANDOM() LIMIT 1")
    question = c.fetchone()
    c.execute("SELECT section_title, chapter_id FROM Sections WHERE section_id=?", (question[1],))
    section = c.fetchone()
    c.execute("SELECT chapter_title FROM Chapters WHERE chapter_id=?", (section[1],))
    chapter = c.fetchone()
    c.execute("SELECT answer_text FROM Answers WHERE question_id=?", (question[2],))
    answers = c.fetchall()
    conn.close()
    return question, section, chapter, answers


def get_section(section_id: int):
    """Retrieve a section from the Sections table in the database."""
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT section_title FROM Sections WHERE section_id=?", (section_id,))
    section = c.fetchone()
    conn.close()
    return section

def get_definitions(term):
    """Retrieve definitions for a given term from the Definitions table in the database."""
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT term, definition_text FROM Definitions WHERE term=?", (term,))
    definitions = c.fetchall()
    conn.close()
    if definitions:
        formatted_definitions = []
        for definition in definitions:
            formatted_definition = format_definition(*definition)
            formatted_definitions.append(formatted_definition)
        return "\n".join(formatted_definitions)
    else:
        return f"No definitions found for {term}."

def format_electrical_knowledge(knowledge: Tuple[int, str, str, str, str]) -> str:
    """Format electrical knowledge retrieved from the electrical_knowledge table in a user-friendly way."""
    id, category, subcategory, content, tags = knowledge
    formatted_knowledge = f"**{id}. {content}**\nCategory: {category}\n"
    if subcategory:
        formatted_knowledge += f"Subcategory: {subcategory}\n"
    if tags:
        formatted_knowledge += f"Tags: {tags}\n"
    return formatted_knowledge

def format_recommended_reading(reading: Tuple[str, str]) -> str:
    """Format recommended reading retrieved from the recommended_reading table in a user-friendly way."""
    title, url = reading
    formatted_reading = f"[{title}]({url})"
    return formatted_reading

def format_webpage_summary(summary: str, url: str) -> str:
    """Format a summary of a webpage retrieved from the WebpageSummary API in a user-friendly way."""
    formatted_summary = f"**Summary:** {summary}\n\n[Read more]({url})"
    return formatted_summary

def format_joke(joke: str) -> str:
    """Format a joke retrieved from a Joke API in a user-friendly way."""
    formatted_joke = f"**Joke:** {joke}"
    return formatted_joke
