# Script name: InventoryControlCommands.py
# Location: gui\Sparky\settings\commands
# Purpose: Allows AI to use functions related to inventory control

import sqlite3
import os

# Define the database path
db_path = os.path.join("databases", "company_name.db")

class InventoryControl:
    def __enter__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def add_item(self, item_name, description, quantity, unit_cost, location):
        with self:
            # Insert item data into the inventory table
            insert_query = "INSERT INTO inventory (item_name, description, quantity, unit_cost, location) VALUES (?, ?, ?, ?, ?)"
            self.cursor.execute(insert_query, (item_name, description, quantity, unit_cost, location))

            # Retrieve the newly created item ID
            item_id = self.cursor.lastrowid

            # Commit changes to the database
            self.connection.commit()

            # Return the newly created item ID
            return item_id

    def update_item(self, item_id, item_name=None, description=None, quantity=None, unit_cost=None, location=None):
        with self:
            # Update the item data in the inventory table
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

            # Remove the trailing comma and space
            update_query = update_query[:-2]

            # Add the item ID to the update query
            update_query += " WHERE item_id = ?"
            update_data.append(item_id)

            # Execute the update query
            self.cursor.execute(update_query, tuple(update_data))

            # Commit changes to the database
            self.connection.commit()

    def delete_item(self, item_id):
        with self:
            # Delete the item from the inventory table
            delete_query = "DELETE FROM inventory WHERE item_id = ?"
            self.cursor.execute(delete_query, (item_id,))

            # Commit changes to the database
            self.connection.commit()

    def get_item(self, item_id):
        # Retrieve item data from the inventory table
        item_query = "SELECT * FROM inventory WHERE item_id = ?"
        self.cursor.execute(item_query, (item_id,))
        item_data = self.cursor.fetchone()

        # Return a dictionary containing the item data
        item_dict = {
            'item_id': item_data[0],
            'item_name': item_data[1],
            'description': item_data[2],
            'quantity': item_data[3],
            'unit_cost': item_data[4],
            'location': item_data[5]
        }
        return item_dict

    def __del__(self):
        self.connection.close()

    def add_item(item_name, description, quantity, unit_cost, location):
        inventory_control = InventoryControl()
        with inventory_control:
            # Check if the item already exists in the inventory
            check_query = "SELECT COUNT(*) FROM inventory WHERE item_name = ?"
            inventory_control.cursor.execute(check_query, (item_name,))
            count = inventory_control.cursor.fetchone()[0]
            if count > 0:
                return f"Error: Item '{item_name}' already exists in the inventory."

            # Add the item to the inventory
            insert_query = "INSERT INTO inventory (item_name, description, quantity, unit_cost, location) VALUES (?, ?, ?, ?, ?)"
            inventory_control.cursor.execute(insert_query, (item_name, description, quantity, unit_cost, location))
            inventory_control.connection.commit()

            return f"Item '{item_name}' added to the inventory."

    def update_item(item_id, item_name=None, description=None, quantity=None, unit_cost=None, location=None):
        inventory_control = InventoryControl()
        with inventory_control:
            # Check if the item exists in the inventory
            check_query = "SELECT COUNT(*) FROM inventory WHERE item_id = ?"
            inventory_control.cursor.execute(check_query, (item_id,))
            count = inventory_control.cursor.fetchone()[0]
            if count == 0:
                return f"Error: Item with ID {item_id} does not exist in the inventory."

            # Update the item in the inventory
            update_query = "UPDATE inventory SET "
            update_values = []
            if item_name is not None:
                update_query += "item_name = ?, "
                update_values.append(item_name)
            if description is not None:
                update_query += "description = ?, "
                update_values.append(description)
            if quantity is not None:
                update_query += "quantity = ?, "
                update_values.append(quantity)
            if unit_cost is not None:
                update_query += "unit_cost = ?, "
                update_values.append(unit_cost)
            if location is not None:
                update_query += "location = ?, "
                update_values.append(location)
            # Remove the trailing comma and space
            update_query = update_query[:-2]
            update_query += " WHERE item_id = ?"
            update_values.append(item_id)

            inventory_control.cursor.execute(update_query, tuple(update_values))
            inventory_control.connection.commit()

            return f"Item with ID {item_id} updated in the inventory."

    def delete_item(item_id):
        inventory_control = InventoryControl()
        with inventory_control:
            # Check if the item exists in the inventory
            check_query = "SELECT COUNT(*) FROM inventory WHERE item_id = ?"
            inventory_control.cursor.execute(check_query, (item_id,))
            count = inventory_control.cursor.fetchone()[0]
            if count == 0:
                return f"Error: Item with ID {item_id} does not exist in the inventory."

            # Delete the item from the inventory
            delete_query = "DELETE FROM inventory WHERE item_id = ?"
            inventory_control.cursor.execute(delete_query, (item_id,))
            inventory_control.connection.commit()

            return f"Item with ID {item_id} deleted from the inventory."

    def get_item(item_id):
        inventory_control = InventoryControl()
        with inventory_control:
            # Check if the item exists in the inventory
            check_query = "SELECT COUNT(*) FROM inventory WHERE item_id = ?"
            inventory_control.cursor.execute(check_query, (item_id,))
            item_count = inventory_control.cursor.fetchone()[0]

            # If the item exists, retrieve its data from the inventory table
            if item_count > 0:
                item_query = "SELECT * FROM inventory WHERE item_id = ?"
                inventory_control.cursor.execute(item_query, (item_id,))
                item_data = inventory_control.cursor.fetchone()
                item_dict = {
                    'item_id': item_data[0],
                    'item_name': item_data[1],
                    'description': item_data[2],
                    'quantity': item_data[3],
                    'unit_cost': item_data[4],
                    'location': item_data[5]
                }
                return item_dict
            else:
                return None
