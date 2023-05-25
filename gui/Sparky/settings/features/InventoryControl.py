# Script name : InventoryControl.py
# location = gui\Sparky\settings\features\InventoryControl.py
# Function = handle_inventory
# accessable from Libraries = 


import sqlite3
import os

db_path = os.path.join("databases", "company_name.db")

class InventoryControl:
    def __init__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def add_item(self, item_name, description, quantity, unit_cost, location):
        insert_query = "INSERT INTO inventory (item_name, description, quantity, unit_cost, location) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(insert_query, (item_name, description, quantity, unit_cost, location))
        self.connection.commit()
        item_id = self.cursor.lastrowid
        return item_id

    def update_item(self, item_id, item_name=None, description=None, quantity=None, unit_cost=None, location=None):
        update_query = "UPDATE inventory SET "
        update_data = []
        if item_name is not None:
            update_query += "item_name = ?, "
            update_data.append(item_name)
        if description is not None:
            update_query += "description = ?, "
            update_data.append(description)
        if quantity is not None:
            update_query += "quantity = ?, "
            update_data.append(quantity)
        if unit_cost is not None:
            update_query += "unit_cost = ?, "
            update_data.append(unit_cost)
        if location is not None:
            update_query += "location = ?, "
            update_data.append(location)
        update_query = update_query.rstrip(", ")
        update_query += " WHERE item_id = ?"
        update_data.append(item_id)
        self.cursor.execute(update_query, tuple(update_data))
        self.connection.commit()

    def delete_item(self, item_id):
        delete_query = "DELETE FROM inventory WHERE item_id = ?"
        self.cursor.execute(delete_query, (item_id,))
        self.connection.commit()

    def get_item(self, item_id):
        item_query = "SELECT * FROM inventory WHERE item_id = ?"
        self.cursor.execute(item_query, (item_id,))
        item_data = self.cursor.fetchone()
        if item_data is None:
            return None
        item_dict = {
            'item_id': item_data[0],
            'item_name': item_data[1],
            'description': item_data[2],
            'quantity': item_data[3],
            'unit_cost': item_data[4],
            'location': item_data[5]
        }
        return item_dict
