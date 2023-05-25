import sqlite3
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QFormLayout, QGroupBox, QHBoxLayout
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase

class QuoteTasksDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quote Tasks")
        self.setGeometry(100, 100, 1200, 600)

        main_layout = QHBoxLayout()

        # Table view for quotes
        self.quote_table = QTableView()
        self.quote_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.quote_table.setSortingEnabled(True)
        self.quote_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.quote_table)

        # Forms and buttons layout
        right_layout = QVBoxLayout()

        # Forms for input
        form_layout = QFormLayout()

        self.project_id_input = QLineEdit()
        self.client_id_input = QLineEdit()
        self.quote_date_input = QLineEdit()
        self.expiration_date_input = QLineEdit()
        self.total_cost_input = QLineEdit()

        form_layout.addRow("Project ID:", self.project_id_input)
        form_layout.addRow("Client ID:", self.client_id_input)
        form_layout.addRow("Quote Date (YYYY-MM-DD):", self.quote_date_input)
        form_layout.addRow("Expiration Date (YYYY-MM-DD):", self.expiration_date_input)
        form_layout.addRow("Total Cost:", self.total_cost_input)

        form_group = QGroupBox("Quote Details")
        form_group.setLayout(form_layout)
        right_layout.addWidget(form_group)

        # Buttons
        button_layout = QVBoxLayout()

        self.save_button = QPushButton("Save")
        self.update_button = QPushButton("Update")
        self.load_button = QPushButton("Load")
        self.delete_button = QPushButton("Delete")

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.delete_button)

        button_group = QGroupBox("Actions")
        button_group.setLayout(button_layout)
        right_layout.addWidget(button_group)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        # Connect button signals to the corresponding slots
        self.save_button.clicked.connect(self.new_quote)
        self.update_button.clicked.connect(self.update_quote)
        self.load_button.clicked.connect(self.load_selected_quote)
        self.delete_button.clicked.connect(self.delete_selected_quote)

        # Load initial quote data
        self.load_quotes()

    def db_connect(self):
        db_path = os.path.join('databases', 'company_name.db')
        connection = sqlite3.connect(db_path)
        return connection

    def quote_template(self):
        # Get the quote template from the database "Company_Name.db"
        pass

    def get_quote_details(self, quote_id):
        connection = self.db_connect()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Quotes WHERE quote_id=?", (quote_id,))
        quote = cursor.fetchone()
        connection.close()

        if quote:
            self.project_id_input.setText(str(quote[1]))
            self.client_id_input.setText(str(quote[2]))
            self.quote_date_input.setText(quote[3])
            self.expiration_date_input.setText(quote[4])
            self.total_cost_input.setText(str(quote[5]))

    def new_quote(self):
        project_id = self.project_id_input.text()
        client_id = self.client_id_input.text()
        quote_date = self.quote_date_input.text()
        expiration_date = self.expiration_date_input.text()
        total_cost = self.total_cost_input.text()

        connection = self.db_connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Quotes (project_id, client_id, quote_date, expiration_date, total_cost) VALUES (?, ?, ?, ?, ?)", (project_id, client_id, quote_date, expiration_date, total_cost))
        connection.commit()
        connection.close()

        self.load_quotes()

    def update_quote(self, quote_id):
        project_id = self.project_id_input.text()
        client_id = self.client_id_input.text()
        quote_date = self.quote_date_input.text()
        expiration_date = self.expiration_date_input.text()
        total_cost = self.total_cost_input.text()

        connection = self.db_connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE Quotes SET project_id=?, client_id=?, quote_date=?, expiration_date=?, total_cost=? WHERE quote_id=?", (project_id, client_id, quote_date, expiration_date, total_cost, quote_id))
        connection.commit()
        connection.close()

        self.load_quotes()

    def delete_quote(self, quote_id):
        connection = self.db_connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Quotes WHERE quote_id=?", (quote_id,))
        connection.commit()
        connection.close()

        self.load_quotes()

    def load_quotes(self):
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(os.path.join('databases', 'company_name.db'))
        db.open()

        self.model = QSqlTableModel(db=db)
        self.model.setTable('Quotes')
        self.model.select()

        self.quote_table.setModel(self.model)

    def load_selected_quote(self):
        selected_rows = self.quote_table.selectionModel().selectedRows()
        if selected_rows:
            quote_id = selected_rows[0].data()
            self.get_quote_details(quote_id)

    def delete_selected_quote(self):
        selected_rows = self.quote_table.selectionModel().selectedRows()
        if selected_rows:
            quote_id = selected_rows[0].data()
            self.delete_quote(quote_id)