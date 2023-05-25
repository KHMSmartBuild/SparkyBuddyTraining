import os
import sys
import re
import importlib
import inspect
import sqlite3

def generate_function_explanations(module):
    """
    Generate explanations for the functions in the given module.

    Args:
        module: The module to generate explanations for.

    Returns:
        A list of tuples, where each tuple represents a function and its explanation.
        Each tuple has the format (name, signature, description).
    """
    explanations = []

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            # Get the function's signature
            signature = inspect.signature(obj)
            explanation = f"Function: {name}{signature}"
            docstring = inspect.getdoc(obj)

            if docstring:
                explanation += f"\nDescription: {docstring.strip()}\n"
            else:
                explanation += "\nDescription: No description provided.\n"

            explanations.append((name, str(signature), docstring))

    return explanations

def store_function_explanations(conn, explanations):
    """
    Store the given function explanations in an SQLite database.

    Args:
        conn: The SQLite connection to use.
        explanations: A list of tuples representing function explanations.
        Each tuple has the format (name, signature, description).
    """
    cursor = conn.cursor()

    # Create the functions table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS functions (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        signature TEXT NOT NULL,
        description TEXT
    )
    """)

    # Add an index for the 'name' column to improve search performance
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_function_name ON functions (name)
    """)

    # Insert the function explanations into the table
    cursor.executemany("""
    INSERT INTO functions (name, signature, description)
    VALUES (?, ?, ?)
    """, explanations)

    # Commit the changes
    conn.commit()

if __name__ == "__main__":
    # Get the path to the libraries folder and the init file
    libraries_path = os.path.join("libraries")
    init_file_path = os.path.join(libraries_path, "__init__.py")

    # Extract module name from the init file path
    module_name = re.sub(r"[/\\]", ".", init_file_path)[:-3]

    # Add the libraries folder to the Python path
    sys.path.append(os.path.abspath(libraries_path))

    # Import the module
    module = importlib.import_module("__init__")

    # Generate explanations for the functions in the module
    explanations = generate_function_explanations(module)

    # Store the explanations in an SQLite database
    db_folder = "databases"
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, "function_explanations.db")
    with sqlite3.connect(db_path) as conn:
        store_function_explanations(conn, explanations)
        print(f"Function explanations stored in {db_path}")
