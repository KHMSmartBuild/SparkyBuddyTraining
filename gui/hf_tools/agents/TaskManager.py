import json
import csv
from datetime import datetime
import uuid

class Task:
     def __init__(self, title, description, due_date, priority, status, project, assignee):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if isinstance(due_date, str) else due_date
        self.priority = priority
        self.status = status
        self.project = project
        self.assignee = assignee

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.users = []

    def create_task(self, title, description, due_date, priority, status, project, assignee):
        task = Task(title, description, due_date, priority, status, project, assignee)
        self.tasks.append(task)

    def assign_task(self, task_id, assignee):
        self.tasks[task_id].assignee = assignee

    def update_task_status(self, task_id, status):
        self.tasks[task_id].status = status

    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

    def get_tasks_by_project(self, project):
        return [task for task in self.tasks if task.project == project]

    def get_tasks_by_assignee(self, assignee):
        return [task for task in self.tasks if task.assignee == assignee]

    def search_tasks(self, query):
        return [task for task in self.tasks if query.lower() in task.title.lower() or query.lower() in task.description.lower()]

    def export_tasks_to_json(self, file_name):
        tasks_data = [task.__dict__ for task in self.tasks]
        with open(file_name, 'w') as file:
            json.dump(tasks_data, file)

    # Update import_tasks_from_json to parse due_date as a datetime.date object
    def import_tasks_from_json(self, file_name):
        with open(file_name, 'r') as file:
            tasks_data = json.load(file)

        for task_data in tasks_data:
            task_data['due_date'] = datetime.strptime(task_data['due_date'], "%Y-%m-%d").date()
            task = Task(**task_data)
            self.tasks.append(task)
            
    # Similar functions can be added for CSV import/export
    # export_tasks_to_csv
    def export_tasks_to_csv(self, file_name):
        with open(file_name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'title', 'description', 'due_date', 'priority', 'status', 'project', 'assignee'])
            for task in self.tasks:
                writer.writerow([task.id, task.title, task.description, task.due_date, task.priority, task.status, task.project, task.assignee])

    # import_tasks_from_csv
    def import_tasks_from_csv(self, file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                task = Task(id=row[0], title=row[1], description=row[2], due_date=row[3], priority=row[4], status=row[5], project=row[6], assignee=row[7])
                self.tasks.append(task)

    # import_csv_tasks_from_json
    def import_csv_tasks_from_json(self, file_name):
        with open(file_name, 'r') as file:
            tasks_data = json.load(file)            


# Instantiate the TaskManager and perform operations
task_manager = TaskManager()
task_manager.create_task("Task 1", "Description 1", "2023-05-01", "High", "Not Started", "Project 1", "User 1")
task_manager.create_task("Task 2", "Description 2", "2023-05-02", "Medium", "In Progress", "Project 2", "User 2")
task_manager.update_task_status(1, "Completed")
tasks_by_status = task_manager.get_tasks_by_status("Completed")
tasks_by_project = task_manager.get_tasks_by_project("Project 1")
tasks_by_assignee = task_manager.get_tasks_by_assignee("User 1")
search_results = task_manager.search_tasks("task")
task_manager.export_tasks_to_json("tasks.json")
task_manager.import_tasks_from_json("tasks.json")
