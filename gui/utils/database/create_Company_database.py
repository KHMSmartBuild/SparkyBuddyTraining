import sqlite3
import os

db_path = os.path.join("databases", "company_name.db")

connection = sqlite3.connect(db_path)

cursor = connection.cursor()

# Clients table
cursor.execute('''CREATE TABLE IF NOT EXISTS clients (
    client_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    contact_person TEXT,
    phone TEXT,
    email TEXT
)''')

# Projects table
cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    client_id INTEGER,
    project_name TEXT,
    project_location TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
)''')

# Tasks table
cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY,
    project_id INTEGER,
    task_name TEXT,
    description TEXT,
    assigned_to TEXT,
    due_date TEXT,
    status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
)''')

# Quotes table
cursor.execute('''CREATE TABLE IF NOT EXISTS quotes (
    quote_id INTEGER PRIMARY KEY,
    project_id INTEGER,
    client_id INTEGER,
    quote_date TEXT,
    expiration_date TEXT,
    total_cost REAL,
    status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
)''')

# Quote_Items table
cursor.execute('''CREATE TABLE IF NOT EXISTS quote_items (
    item_id INTEGER PRIMARY KEY,
    quote_id INTEGER,
    description TEXT,
    quantity INTEGER,
    unit_price REAL,
    total_price REAL,
    FOREIGN KEY (quote_id) REFERENCES quotes (quote_id)
)''')

# Invoices table
cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
    invoice_id INTEGER PRIMARY KEY,
    project_id INTEGER,
    client_id INTEGER,
    invoice_date TEXT,
    due_date TEXT,
    total_cost REAL,
    status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (project_id),
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
)''')

# Invoice_Items table
cursor.execute('''CREATE TABLE IF NOT EXISTS invoice_items (
    item_id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    description TEXT,
    quantity INTEGER,
    unit_price REAL,
    total_price REAL,
    FOREIGN KEY (invoice_id) REFERENCES invoices (invoice_id)
)''')

# Payments table
cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    invoice_id INTEGER,
    client_id INTEGER,
    payment_date TEXT,
    amount REAL,
    method TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices (invoice_id),
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
)''')

# Inventory table
cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT,
    description TEXT,
    quantity INTEGER,
    unit_cost REAL,
    location TEXT
)''')

# Suppliers table
cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    contact_person TEXT,
    phone TEXT,
    email TEXT
)''')

# Employees table
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    address TEXT,
    phone TEXT,
    email TEXT,
    hire_date TEXT,
    position TEXT,
    hourly_rate REAL
)''')

# Work_Hours table
cursor.execute('''CREATE TABLE IF NOT EXISTS work_hours (
    record_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_id INTEGER,
    date TEXT,
    hours_worked REAL,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
)''')

# Add other tables here using the same format

# Commit and close the connection
connection.commit()
connection.close()
