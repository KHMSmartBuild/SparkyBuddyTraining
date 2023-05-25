# Script name : Quoting.py
# location = gui\Sparky\sparky_features.py
# Function = Create quotes for jobs and apppend to quotes table
# accessable from Libraries = yes

from Sparky_commands import *
import sqlite3
import os
from datetime import datetime, timedelta

class Quoting:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_quote(self, project_id, client_id, quote_items):
        """
        Create a quote based on project information and quote items.
        :param project_id: ID of the project.
        :param client_id: ID of the client.
        :param quote_items: List of dictionaries containing quote item information.
        :return: ID of the created quote.
        """
        # Calculate the total cost of the quote based on the quote items
        total_cost = sum([item['total_price'] for item in quote_items])

        # Insert the quote into the database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        quote_date = datetime.now().strftime('%Y-%m-%d')
        expiration_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        status = 'draft'
        c.execute("INSERT INTO quotes (project_id, client_id, quote_date, expiration_date, total_cost, status) VALUES (?, ?, ?, ?, ?, ?)", (project_id, client_id, quote_date, expiration_date, total_cost, status))
        quote_id = c.lastrowid

        # Insert the quote items into the database
        for item in quote_items:
            c.execute("INSERT INTO quote_items (quote_id, description, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)", (quote_id, item['description'], item['quantity'], item['unit_price'], item['total_price']))

        conn.commit()
        conn.close()

        # Return the ID of the created quote
        return quote_id

    def update_quote(self, quote_id, quote_items):
        """
        Update an existing quote with new quote items.
        :param quote_id: ID of the quote to update.
        :param quote_items: List of dictionaries containing updated quote item information.
        """
        # Calculate the total cost of the quote based on the quote items
        total_cost = sum([item['total_price'] for item in quote_items])

        # Update the quote in the database
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE quotes SET total_cost = ? WHERE quote_id = ?", (total_cost, quote_id))

        # Delete the existing quote items from the database
        c.execute("DELETE FROM quote_items WHERE quote_id = ?", (quote_id,))

        # Insert the updated quote items into the database
        for item in quote_items:
            c.execute("INSERT INTO quote_items (quote_id, description, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)", (quote_id, item['description'], item['quantity'], item['unit_price'], item['total_price']))

        conn.commit()
        conn.close()

    def get_quote(self, quote_id):
        """
        Retrieve a quote from the database using the quote_id.
        :param quote_id: ID of the quote to retrieve.
        :return: Dictionary containing the quote information.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        # Retrieve the quote information from the database
        c.execute("SELECT * FROM quotes WHERE quote_id = ?", (quote_id,))
        quote = c.fetchone()
        if not quote:
            return None

        # Retrieve the quote items from the database
        c.execute("SELECT * FROM quote_items WHERE quote_id = ?", (quote_id,))
        quote_items = c.fetchall()
        if not quote_items:
            return None
        
            # Format the quote information and quote items as a dictionary
        quote_info = {
            'quote_id': quote[0],
            'project_id': quote[1],
            'client_id': quote[2],
            'quote_date': quote[3],
            'expiration_date': quote[4],
            'total_cost': quote[5],
            'status': quote[6],
            'quote_items': []
        }
        for item in quote_items:
            quote_info['quote_items'].append({
                'item_id': item[0],
                'quote_id': item[1],
                'description': item[2],
                'quantity': item[3],
                'unit_price': item[4],
                'total_price': item[5]
            })

        conn.close()



        

