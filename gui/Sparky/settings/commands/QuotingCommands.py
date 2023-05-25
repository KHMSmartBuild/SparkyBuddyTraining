# Script name: QuotingCommands.py
# Location : gui\Sparky\settings\commands
# purpose: Allows Ai to use functions


import sqlite3
import os

# Define the database path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "databases", "company_name.db"))
class Quoting:
    def __init__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def create_quote(self, client_info, quote_text, items):
     if not isinstance(client_info, str) or not isinstance(quote_text, str) or not isinstance(items, list):
        raise ValueError("Invalid input parameters")
     try:
        with self:
            # Insert quote data into the quotes table
            insert_query = "INSERT INTO quotes (client_info, quote_text) VALUES (?, ?)"
            self.cursor.execute(insert_query, (client_info, quote_text))
            
            # Retrieve the newly created quote ID
            quote_id = self.cursor.lastrowid

            # Insert quote item data into the quote_items table
            for item in items:
                item_query = "INSERT INTO quote_items (quote_id, item_name, item_quantity, item_price) VALUES (?, ?, ?, ?)"
                self.cursor.execute(item_query, (quote_id, item['name'], item['quantity'], item['price']))

            # Commit changes to the database
            self.connection.commit()

            # Return the newly created quote ID
            return quote_id
        
     except sqlite3.Error as e:
        print(f"Database error: {e}")        

    def update_quote(self, quote_id, quote_text):
        # Update the quote text in the quotes table
        update_query = "UPDATE quotes SET quote_text = ? WHERE quote_id = ?"
        self.cursor.execute(update_query, (quote_text, quote_id))
        
        # Commit changes to the database
        self.connection.commit()
    
    def get_quote(self, quote_id):
        # Retrieve quote data and quote item data from the quotes and quote_items tables
        quote_query = """
            SELECT quotes.*, quote_items.item_name, quote_items.item_quantity, quote_items.item_price 
            FROM quotes JOIN quote_items ON quotes.quote_id = quote_items.quote_id 
            WHERE quotes.quote_id = ?
        """
        self.cursor.execute(quote_query, (quote_id,))
        quote_data = self.cursor.fetchall()

        # Convert the quote item data into a list of dictionaries
        quote_item_list = []
        for item in quote_data:
            item_dict = {
                'name': item[2],
                'quantity': item[3],
                'price': item[4]
            }
            quote_item_list.append(item_dict)

        # Return a dictionary containing the quote data and quote item data
        quote_dict = {
            'quote_id': quote_data[0][0],
            'client_info': quote_data[0][1],
            'quote_text': quote_data[0][2],
            'quote_items': quote_item_list
        }
        return quote_dict

    def __del__(self):
        self.connection.close()

# Define the commands for creating, updating, and getting quotes
def create_quote(client_info, quote_text, items):
    quoting = Quoting()
    return quoting.create_quote(client_info, quote_text, items)

def update_quote(quote_id, quote_text):
    quoting = Quoting()
    quoting.update_quote(quote_id, quote_text)

def get_quote(quote_id):
    quoting = Quoting()
    return quoting.get_quote(quote_id)

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