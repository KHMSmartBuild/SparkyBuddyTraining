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
            'first_name': employee_data[1].strip(),
            'last_name': employee_data[2].strip(),
            'address': employee_data[3].strip(),
            'phone': employee_data[4].strip(),
            'email': employee_data[5].strip(),
            'hire_date': employee_data[6].strip(),
            'position': employee_data[7].strip(),
            'hourly_rate': employee_data[8]
            }
        return employee_dict

    def get_employee_id(self, first_name, last_name):
        # Retrieve employee ID from the employees table
        employee_id_query = "SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?"
        self.cursor.execute(employee_id_query, (first_name.strip(), last_name.strip()))
        employee_id_data = self.cursor.fetchone()

        # Return the employee ID
        if employee_id_data is not None:
            return employee_id_data[0]
        else:
            return None

    def add_work_hours(self, employee_id, project_id, date, hours_worked):
        with self:
            # Insert work hour data into the work_hours table
            insert_query = "INSERT INTO work_hours (employee_id, project_id, date, hours_worked) VALUES (?, ?, ?, ?)"
            self.cursor.execute(insert_query, (employee_id, project_id, date, hours_worked))

            # Retrieve the newly created record ID
            record_id = self.cursor.lastrowid

            # Commit changes to the database
            self.connection.commit()

            # Return the newly created record ID
            return record_id

    def update_work_hours(self, record_id, employee_id=None, project_id=None, date=None, hours_worked=None):
        with self:
            # Update the work hour data in the work_hours table
            update_query = "UPDATE work_hours SET "
            update_data = []
            if employee_id is not None:
                update_query += "employee_id = ?, "
                update_data.append(employee_id)
            if project_id is not None:
                update_query += "project_id = ?, "
                update_data.append(project_id)
            if date is not None:
                update_query += "date = ?, "
                update_data.append(date)
            if hours_worked is not None:
                update_query += "hours_worked = ?, "
                update_data.append(hours_worked)

            # Remove the trailing comma and space
            update_query = update_query[:-2]

            # Add the record ID to the update query
            update_query += " WHERE record_id = ?"
            update_data.append(record_id)

            # Execute the update query
            self.cursor.execute(update_query, tuple(update_data))

            # Commit changes to the database
            self.connection.commit()

    def delete_work_hours(self, record_id):
        with self:
            # Delete the work hour record from the work_hours table
            delete_query = "DELETE FROM work_hours WHERE record_id = ?"
            self.cursor.execute(delete_query, (record_id,))

            # Commit changes to the database
            self.connection.commit()

    def add_deduction(self, employee_id, date, description, amount):
        with self:
            # Insert deduction data into the deductions table
            insert_query = "INSERT INTO deductions (employee_id, date, description, amount) VALUES (?, ?, ?, ?)"
            self.cursor.execute(insert_query, (employee_id, date, description, amount))

            # Retrieve the newly created record ID
            record_id = self.cursor.lastrowid

            # Commit changes to the database
            self.connection.commit()

            # Return the newly created record ID
            return record_id

    def update_deduction(self, record_id, employee_id=None, date=None, description=None, amount=None):
        with self:
        # Update the deduction data in the deductions table
         update_query = "UPDATE deductions SET "
        update_data = []
        if employee_id is not None:
         update_query += "employee_id = ?, "
        update_data.append(employee_id)
        if date is not None:
         update_query += "date = ?, "
        update_data.append(date)
        if description is not None:
         update_query += "description = ?, "
        update_data.append(description)
        if amount is not None:
         update_query += "amount = ?, "
        update_data.append(amount)

        # Remove the trailing comma and space
        update_query = update_query[:-2]

        # Add the record ID to the update query
        update_query += " WHERE record_id = ?"
        update_data.append(record_id)

        # Execute the update query
        self.cursor.execute(update_query, tuple(update_data))

        # Commit changes to the database
        self.connection.commit()

    def delete_deduction(self, record_id):
        with self:
            # Delete the deduction from the deductions table
            delete_query = "DELETE FROM deductions WHERE record_id = ?"
            self.cursor.execute(delete_query, (record_id,))

            # Commit changes to the database
            self.connection.commit()

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
