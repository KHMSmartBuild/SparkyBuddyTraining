# Script name : sparky_features.py
# location = gui\Sparky\sparky_features.py
# accessable from Libraries = yes
# Author: KHM Smartbuild
import sys
print(sys.path)
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
features_dir = os.path.join(parent_dir, 'settings', 'features')
sys.path.insert(0, parent_dir)
sys.path.insert(0, features_dir)
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

class Sparky_quoting:
    def __init__(self, username, password, host, port, database):
        # create a connection to the database
        self.engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")
        self.metadata = MetaData()
        self.quotes_table = Table(
            'quotes', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('client_info', String),
            Column('job_details', String),
            Column('cost', Integer)
        )
        self.metadata.create_all(self.engine)

    def create_quote(self, client_info, job_details):
        """
        Create a quote based on client information and job details.
        :param client_info: Dictionary containing client information.
        :param job_details: Dictionary containing job details.
        :return: Dictionary containing the quote information.
        """
        # Calculate the cost of the quote based on the job details
        cost = 0
        if job_details.get('repair'):
            cost += 50
        if job_details.get('installation'):
            cost += 100
        if job_details.get('fault_finding'):
            cost += 75
        if job_details.get('testing'):
            cost += 25

        # Add a markup to the cost based on the client information
        if client_info.get('is_vip'):
            cost *= 1.1
        else:
            cost *= 1.2

        # Insert the quote into the database
        conn = self.engine.connect()
        ins = self.quotes_table.insert().values(client_info=str(client_info), job_details=str(job_details), cost=cost)
        conn.execute(ins)

        # Return the quote information
        quote_info = {
            'client_info': client_info,
            'job_details': job_details,
            'cost': cost
        }
        return quote_info

    def update_quote(self, quote_id, updated_info):
        """
        Update an existing quote with new information.
        :param quote_id: ID of the quote to update.
        :param updated_info: Dictionary containing updated information.
        :return: Dictionary containing the updated quote information.
        """
        # Retrieve the quote information from the database using quote_id
        conn = self.engine.connect()
        sel = self.quotes_table.select().where(self.quotes_table.c.id == quote_id)
        result = conn.execute(sel)
        quote_info = result.fetchone()

        # Update the quote information with the new information
        if 'client_info' in updated_info:
            quote_info['client_info'] = str(updated_info['client_info'])
        if 'job_details' in updated_info:
            quote_info['job_details'] = str(updated_info['job_details'])
        if 'cost' in updated_info:
            quote_info['cost'] = updated_info['cost']

        # Save the updated quote information to the database
        upd = self.quotes_table.update().values(client_info=quote_info['client_info'], job_details=quote_info['job_details'], cost=quote_info['cost']).where(self.quotes_table.c.id == quote_id)
        conn.execute(upd)

        # Return the updated quote information
        return quote_info

    def get_quote(self, quote_id):
        """
        Retrieve a quote from the database using the quote_id.
        :param quote_id: ID of the quote to retrieve.
        :return: Dictionary containing the quote information.
        """
        conn = self.engine.connect()
        sel = self.quotes_table.select().where(self.quotes_table.c.id == quote_id)

        # Retrieve the quote information from the database using quote_id
        result = conn.execute(sel)
        quote_info = result.fetchone()
        return quote_info


# Class for handling inventory control
class Sparky_InventoryControl:
    def __init__(self):
        self.conn = self.engine.connect('company_name.db')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def add_item(self, item):
        """
        Add an item to the inventory.
        :param item: Dictionary containing item information.
        :return: None
        """
        self.cursor.execute("INSERT INTO inventory VALUES (?, ?, ?)", (item['id'], item['name'], item['quantity']))
        self.conn.commit()

    def remove_item(self, item_id):
        """
        Remove an item from the inventory.
        :param item_id: ID of the item to remove.
        :return: None
        """
        self.cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        self.conn.commit()

# Class for handling payroll
class Sparky_Payroll:
    def __init__(self):
        self.hourly_rate = 35.0
        self.salary = 50000.0
        self.sub_contractor_rate = 60.0
        self.uk_tax_rate = 0.08
        self.cis_rate = 0.3
        self.vat_rate = 0.2

    def calculate_pay(self, employee_id, hours_worked, is_hourly=False, is_salary=False, is_sub_contractor=False):
        """
        Calculate the pay for an employee based on hours worked.
        :param employee_id: ID of the employee.
        :param hours_worked: Number of hours worked.
        :param is_hourly: True if employee is paid hourly, False otherwise.
        :param is_salary: True if employee is paid a salary, False otherwise.
        :param is_sub_contractor: True if employee is a sub-contractor, False otherwise.
        :return: float representing the pay amount.
        """
        if is_hourly:
            pay = hours_worked * self.hourly_rate
        elif is_salary:
            pay = self.salary / 12  # Monthly salary
        elif is_sub_contractor:
            pay = hours_worked * self.sub_contractor_rate

            # Deductions
            pay -= pay * self.uk_tax_rate
            pay -= pay * self.cis_rate
            pay += pay * self.vat_rate
        else:
            raise ValueError("Employee must be hourly, salaried, or a sub-contractor.")

        return pay

        # You can call the method with the appropriate parameters 
        # to calculate the pay for different types of employees.
        #  For example:

        """

        payroll = Payroll()

        # Calculate pay for an hourly employee who worked 40 hours
        hourly_pay = payroll.calculate_pay(employee_id=1, hours_worked=40, is_hourly=True)

        # Calculate pay for a salaried employee
        salary_pay = payroll.calculate_pay(employee_id=2, hours_worked=None, is_salary=True)

        # Calculate pay for a sub-contractor who worked 40 hours
        sub_contractor_pay = payroll.calculate_pay(employee_id=3, hours_worked=40, is_sub_contractor=True)


        """

# Class for handling job scheduling
class Sparky_JobScheduling:
    def __init__(self):
        pass

    def schedule_job(self, job_info):
        """
        Schedule a job based on the provided information.
        :param job_info: Dictionary containing job information.
        :return: None
        """
        # Get available employees based on job time
        available_employees = self.get_available_employees(job_info['start_time'], job_info['end_time'])
        if not available_employees:
            # No available employees for the given time range
            return

        # Match job with most suitable employee
        employee = self.match_job_with_employee(job_info, available_employees)
        if not employee:
            # No suitable employee found
            return

        # Update employee schedule and assign job
        self.update_employee_schedule(employee, job_info)
        employee.assign_job(job_info)

# Class for handling customer care
class Sparky_CustomerCare:
    def __init__(self):
        pass

    def create_ticket(self, issue_info):
        """
        Create a customer support ticket based on the provided issue information.
        :param issue_info: Dictionary containing issue information.
        :return: None
        """
        # TODO: Implement the ticket creation logic
        pass

    def update_ticket(self, ticket_id, updated_info):
        """
        Update an existing ticket with new information.
        :param ticket_id: ID of the ticket to update.
        :param updated_info: Dictionary containing updated information.
        :return: None
        """
        # TODO: Implement the ticket update logic
        pass

# Class for connecting to IoT devices
class Sparky_IoTConnection:
    def __init__(self):
        pass

    def connect_device(self, device_id):
        """
        Connect to an IoT device with the given device ID.
        :param device_id: ID of the device to connect.
        :return: None
        """
        # TODO: Implement the IoT device connection logic
        pass

def disconnect_device(self, device_id):
    """
    Disconnect from an IoT device with the given device ID.
    :param device_id: ID of the device to disconnect.
    :return: None
    """
    # TODO: Implement the IoT device disconnection logic
    pass

# class for handling electrical theory
class Sparky_ElectricalTheory:
    def calculate_power_factor(self, real_power, apparent_power):
        """
        Calculate the power factor based on real power and apparent power.
        :param real_power: float representing real power (in watts).
        :param apparent_power: float representing apparent power (in volt-amperes).
        :return: float representing the power factor.
        """
        if apparent_power == 0:
            return 0
        return abs(real_power / apparent_power)

    def calculate_voltage_drop(self, current, resistance, distance):
        """
        Calculate the voltage drop based on current, resistance, and distance.
        :param current: float representing current (in amperes).
        :param resistance: float representing resistance (in ohms).
        :param distance: float representing distance (in meters).
        :return: float representing the voltage drop (in volts).
        """
        return current * resistance * distance

    def calculate_short_circuit_current(self, voltage, impedance):
        """
        Calculate the short-circuit current based on voltage and impedance.
        :param voltage: float representing voltage (in volts).
        :param impedance: float representing impedance (in ohms).
        :return: float representing the short-circuit current (in amperes).
        """
        if impedance != 0:
            return voltage / impedance
        return float('inf')


