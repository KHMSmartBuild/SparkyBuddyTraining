# Script name: PayrollCommands.py
# Location: gui\Sparky\settings\commands
# Purpose: Allows AI to use functions related to payroll

import sqlite3
import os

# Define the database path
db_path = os.path.join("databases", "company_name.db")

class Payroll:
    def __enter__(self):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()

    def add_employee(self, first_name, last_name, address, phone, email, hire_date, position, hourly_rate):
        with self:
            # Insert employee data into the employees table
            insert_query = "INSERT INTO employees (first_name, last_name, address, phone, email, hire_date, position, hourly_rate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            self.cursor.execute(insert_query, (first_name, last_name, address, phone, email, hire_date, position, hourly_rate))

            # Retrieve the newly created employee ID
            employee_id = self.cursor.lastrowid

            # Commit changes to the database
            self.connection.commit()

            # Return the newly created employee ID
            return employee_id

    def update_employee(self, employee_id, first_name=None, last_name=None, address=None, phone=None, email=None, hire_date=None, position=None, hourly_rate=None):
        with self:
            # Update the employee data in the employees table
            update_query = "UPDATE employees SET "
            update_data = []
            if first_name is not None:
                update_query += "first_name = ?, "
                update_data.append(first_name)
            if last_name is not None:
                update_query += "last_name = ?, "
                update_data.append(last_name)
            if address is not None:
                update_query += "address = ?, "
                update_data.append(address)
            if phone is not None:
                update_query += "phone = ?, "
                update_data.append(phone)
            if email is not None:
                update_query += "email = ?, "
                update_data.append(email)
            if hire_date is not None:
                update_query += "hire_date = ?, "
                update_data.append(hire_date)
            if position is not None:
                update_query += "position = ?, "
                update_data.append(position)
            if hourly_rate is not None:
                update_query += "hourly_rate = ?, "
                update_data.append(hourly_rate)

            # Remove the trailing comma and space
            update_query = update_query[:-2]

            # Add the employee ID to the update query
            update_query += " WHERE employee_id = ?"
            update_data.append(employee_id)

            # Execute the update query
            self.cursor.execute(update_query, tuple(update_data))

            # Commit changes to the database
            self.connection.commit()

    def delete_employee(self, employee_id):
        with self:
            # Delete the employee from the employees table
            delete_query = "DELETE FROM employees WHERE employee_id = ?"
            self.cursor.execute(delete_query, (employee_id,))

            # Commit changes to the database
            self.connection.commit()

    def get_employee(self, employee_id):
        # Retrieve employee data from the employees table
        employee_query = "SELECT * FROM employees WHERE employee_id = ?"
        self.cursor.execute(employee_query, (employee_id,))
        employee_data = self.cursor.fetchone()

        # Return a dictionary containing the employee data
        employee_dict = {
            'employee_id': employee_data[0],
            'first_name': employee_data[1],
            'last_name': employee_data[2],
            'address': employee_data[3],
            'phone': employee_data[4],
            'email': employee_data[5],
            'hire_date': employee_data[6],
            'position': employee_data[7],
            'hourly_rate': employee_data[8]
        }
        return employee_dict

    def get_employee_work_hours(self, employee_id, start_date=None, end_date=None):
        # Retrieve work hour data for the employee from the work_hours table
        work_hour_query = "SELECT * FROM work_hours WHERE employee_id = ?"
        query_args = [employee_id]

        # If start_date is provided, add it as a filter to the query
        if start_date is not None:
            work_hour_query += " AND date >= ?"
            query_args.append(start_date)

        # If end_date is provided, add it as a filter to the query
        if end_date is not None:
            work_hour_query += " AND date <= ?"
            query_args.append(end_date)

        self.cursor.execute(work_hour_query, tuple(query_args))
        work_hour_data = self.cursor.fetchall()

        # Return a list of dictionaries containing the work hour data
        work_hour_list = []
        for row in work_hour_data:
            work_hour_dict = {
                'record_id': row[0],
                'employee_id': row[1],
                'project_id': row[2],
                'date': row[3],
                'hours_worked': row[4]
            }
            work_hour_list.append(work_hour_dict)

        return work_hour_list
    
    def get_employee_deductions(self, employee_id, start_date=None, end_date=None):
        # Retrieve deduction data for the employee from the deductions table
        deduction_query = "SELECT * FROM deductions WHERE employee_id = ?"
        query_args = [employee_id]

        # If start_date is provided, add it as a filter to the query
        if start_date is not None:
            deduction_query += " AND date >= ?"
            query_args.append(start_date)

        # If end_date is provided, add it as a filter to the query
        if end_date is not None:
            deduction_query += " AND date <= ?"
            query_args.append(end_date)

        self.cursor.execute(deduction_query, tuple(query_args))
        deduction_data = self.cursor.fetchall()

        # Return a list of dictionaries containing the deduction data
        deduction_list = []
        for row in deduction_data:
            deduction_dict = {
                'record_id': row[0],
                'employee_id': row[1],
                'date': row[2],
                'description': row[3],
                'amount': row[4]
            }
            deduction_list.append(deduction_dict)

        return deduction_list

    def calculate_payroll(self, employee_id, start_date=None, end_date=None):
        # Retrieve the employee's hourly rate
        employee_data = self.get_employee(employee_id)
        hourly_rate = employee_data['hourly_rate']

        # Retrieve the employee's work hours during the specified date range
        work_hours = self.get_employee_work_hours(employee_id, start_date, end_date)

        # Calculate the total number of hours worked by the employee
        total_hours_worked = 0
        for work_hour in work_hours:
            total_hours_worked += work_hour['hours_worked']

        # Calculate the employee's gross pay
        gross_pay = hourly_rate * total_hours_worked

        # Calculate the employee's deductions
        deductions = self.get_employee_deductions(employee_id, start_date, end_date)
        total_deductions = 0
        for deduction in deductions:
            total_deductions += deduction['amount']

        # Calculate the employee's net pay
        net_pay = gross_pay - total_deductions

        # Return a dictionary containing the payroll data
        payroll_dict = {
            'employee_id': employee_id,
            'start_date': start_date,
            'end_date': end_date,
            'hourly_rate': hourly_rate,
            'total_hours_worked': total_hours_worked,
            'gross_pay': gross_pay,
            'total_deductions': total_deductions,
            'net_pay': net_pay
        }
        return payroll_dict
