import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class File:

    def __init__(self, filename):
        self.filename = filename

    def create(self, contents=""):
        """Create a file if it doesn't exist."""
        if not os.path.exists(self.filename):
            self._write(contents)
    
    def _read(self, filename):
        """Read a file from the disk."""
        with open(filename, "r") as file:
            return file.read().split("\n")
        
    def _write(self, contents):
        """Write a file to the disk."""
        with open(self.filename, 'w') as file:
            return file.write(contents)


class User(File):
    
    def get_user(self):
        """Get users' details such as username and password from the file."""
        users = {}
        for item in super()._read("user.txt"):
            username, password = item.split(';')
            users[username] = password
        return users


    def log_in(self):
        """Log in users using username and password"""

        logged_in = False
        while not logged_in:
            print()
            print("***LOGIN***")
            current_user = input("Username: ").strip()
            current_password = input("Password: ").strip()
            if current_user not in self.get_user().keys():
                print(f"{'-'*20}")
                print("User does not exist!")
                print(f"{'-'*20}")
                continue
            elif self.get_user()[current_user] != current_password:
                print(f"{'-'*20}")
                print("Wrong password!")
                print(f"{'-'*20}")
                continue
            else:
                print(f"{'-'*20}")
                print("Login successful!")
                print(f"{'-'*20}")
                logged_in = True
        return current_user


    def register(self):
        '''Register a new user to the 'user.txt' file.'''

        users = self.get_user()

        isExisting = False
        while not isExisting:
            new_username = input("New Username: ")
            if new_username in users.keys():
                print(f"{'-'*20}")
                print("The username is already in use and please enter another username!")
                print(f"{'-'*20}")
                continue
            else:
                isExisting = True

        new_password = input("New Password: ")

        isConfirmed = False
        while not isConfirmed:
            confirm_password = input("Confirm Password: ")
            if confirm_password != new_password:
                print(f"{'-'*20}")
                print("Passwords do not match! Please re-enter password.")
                print(f"{'-'*20}")
                continue
            else:
                print(f"{'-'*20}")
                print("New user is registered successfully!")
                print(f"{'-'*20}")
                users[new_username] = new_password

                user_file = []
                for key in users:
                    user_file.append(f"{key};{users[key]}")
                super()._write("\n".join(user_file))
                
                isConfirmed = True

    
    def user_overview(self, tasks:list):
        """Display task overview reports and save it to user_overview.txt"""

        display = ""
        display += f"{' '*25}User Overview{' '*25}\n"
        display += f"{' '*46}Date: {date.today()}\n" 
        display += f"{'-'*62}\n"
        display += f"Total number of users: \t\t\t\t {len([username for username in self.get_user().keys()])}\n"
        display += f"Total number of tasks: \t\t\t\t {len([task for task in tasks])}\n"
        display += f"\n"
        
        for username in self.get_user().keys():
            assigned_tasks = [task for task in tasks if task['username'] == username]            
            display += f"User: {username}\n"
            display += f"{'-'*12}\n"
            display += f"Total number of tasks assigned: \t\t\t {len(assigned_tasks)}\n"
            display += f"The percentage of tasks assigned: \t\t\t {round(len(assigned_tasks)/len([task for task in tasks]), 2)*100}%\n"
            if len(assigned_tasks) == 0:  # Eliminate zeroDivisionError if no tasks are assigned to user
                assigned_tasks = [1]
            display += f"The percentage of tasks assigned and completed: \t {round(len([task for task in tasks if task['username'] == username and task['completed'] == True])/len(assigned_tasks), 2)*100}%\n"
            display += f"The percentage of tasks must still be completed: \t {round(len([task for task in tasks if task['username'] == username and task['completed'] == False])/len(assigned_tasks), 2)*100}%\n"
            display += f"The percentage of tasks uncompleted and overdue: \t {round(len([task for task in tasks if task['username'] == username and task['completed'] == False and task['due_date'].date() < date.today()])/len(assigned_tasks), 2)*100}%\n"
            display += f"\n"
        
        display += f"{'-'*62}\n"
        print(f"{display}")
        return display


class Task(File):

    has_been_completed = False

    def mark_as_completed(self):
        """Mark the task as"""
        self.has_been_completed = True


    def get_task(self):
        """Read the tasks from the file"""
        _tasks = []
        read_tasks = [item for item in super()._read("tasks.txt") if item != ""]
        for item in read_tasks:
            task = {}
            task['username'] = item.split(";")[0]
            task['title'] = item.split(";")[1]
            task['description'] = item.split(";")[2]
            task['assigned_date'] = datetime.strptime(item.split(';')[4], DATETIME_STRING_FORMAT)
            task['due_date'] = datetime.strptime(item.split(';')[3], DATETIME_STRING_FORMAT)
            task['completed'] = True if item.split(";")[5] == "Yes" else False           
            _tasks.append(task)
        return _tasks
       
    
    def process_task(self, tasks):
        """Update the due date or mark as completed to the file"""

        task_to_write = []
        for task in tasks:
            task_content = [
                task['username'],
                task['title'],
                task['description'],
                task['assigned_date'].strftime(DATETIME_STRING_FORMAT), 
                task['due_date'].strftime(DATETIME_STRING_FORMAT),                 
                "Yes" if task['completed'] else "No"
            ]
            task_to_write.append(";".join(task_content))
        
        return task_to_write


    def add_task(self, users=""):
        """Add the tasks into the file"""
        while True:
            assigned_user = input("Name of person assigned to task: ")
            if assigned_user not in users:
                print("User does not exist. Please enter a valid username!")
                continue
            else:
                break
        
        title = input("Title of Task: ")
        description = input("Description of Task: ")

        while True:
            try:
                task_due = input("Due date of task (YYYY-MM-DD): ")
                due_date = datetime.strptime(task_due, DATETIME_STRING_FORMAT)
                break
            except ValueError:
                print(f"{'-'*20}")
                print("Invalid datetime format. Please use the format specified")
                print(f"{'-'*20}")
        
        # Add the new task into the task file
        _tasks = self.get_task()
        new_task = {
            "username": assigned_user,
            "title": title,
            "description": description,
            "assigned_date": date.today(),
            "due_date": due_date,            
            "completed": False
        }
        _tasks.append(new_task)
 
        # Write the tasks into the file.
        super()._write("\n".join(self.process_task(_tasks)))
        print("Task successfully added.")
      

    def view_all(self, tasks):
        """View the tasks from all users"""
        display = ""
        for task in tasks:
            display += f"\n"
            display += f"{'-'*60}\n"
            display += f"Task Title: \t\t{task['title']}\n"
            display += f"Assigned to: \t\t{task['username']}\n"
            display += f"Date Assigned: \t\t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"  
            display += f"Due Date: \t\t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" 
            display += f"Take Complete?: \t{task['completed']}\n"
            display += f"Task Description: \n   {task['description']}\n"
            display += f"{'-'*60}\n"
        print(f"{display}")


    def view_mine(self, tasks, curr_user):
        """View the tasks from the current users"""
        my_task_count = 0
        display = ""
        for task in tasks:
            if task['username'] == curr_user:
                my_task_count += 1
                display += f"\n"           
                display += f"Task Number(#): {my_task_count}\n"
                display += f"{'-'*60}\n"
                display += f"Task Title: \t\t{task['title']}\n"
                display += f"Assigned to: \t\t{task['username']}\n"
                display += f"Date Assigned: \t\t{task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"  
                display += f"Due Date: \t\t{task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n" 
                display += f"Take Complete?: \t{task['completed']}\n"
                display += f"Task Description: \n   {task['description']}\n"
                display += f"{'-'*60}\n"               
        print(f"{display}")
        return my_task_count
    

    def task_overview(self, tasks):
        """Display task overview reports and save it to task_overview.txt"""

        display = ""
        display += f"{' '*25}Task Overview{' '*25}\n"
        display += f"{' '*46}Date: {date.today()}\n"
        display += f"{'-'*62}\n"
        display += f"Total number of tasks: \t\t\t\t\t {len(tasks)}\n"
        display += f"Total number of completed tasks: \t\t\t {len([task for task in tasks if task['completed'] == True])}\n"
        display += f"Total number of uncompleted tasks: \t\t\t {len([task for task in tasks if task['completed'] == False])}\n"
        display += f"Total number of uncompleted and overdue tasks: \t\t {len([task for task in tasks if task['completed'] == False and task['due_date'].date() < date.today()])}\n"
        display += f"The percentage of incomplete tasks: \t\t\t {round(len([task for task in tasks if task['completed'] == False])/len(tasks), 2)*100}%\n"
        display += f"The percentage of overdue tasks: \t\t\t {round(len([task for task in tasks if task['completed'] == False and task['due_date'].date() < date.today()])/len(tasks), 2)*100}%\n"
        display += f"{'-'*62}\n"      
        print(f"{display}")
        return display
        

if __name__ == '__main__':

    # Create tasks.txt file if it doesn't exist
    task_file = File("tasks.txt")
    task_file.create()
    
    # Read tasks.txt to get the tasks
    task = Task("tasks.txt")
    tasks = task.get_task()

    #====Login Section====
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    # Create user.txt if it doesn't exist
    user_file = File("user.txt")
    user_file.create("admin;password")
    
    # User login
    user = User("user.txt")
    users = user.get_user()
    current_user = user.log_in()
    
    # Presenting the menu to the user
    while True:
        print()
        menu = input('''Select one of the following Options below:
  re - register a user
  ad - add a task
  va - view all tasks
  vm - view my task
  gr - generate reports
  ds - display statistics
  ex - Exit
  ::>>> ''').lower()
        
        # Register a user
        if menu == "re":
            user.register()

        # Add a task
        elif menu == "ad":
            task.add_task(user.get_user())
        
        # View all tasks
        elif menu == "va":
            task.view_all(task.get_task())
        
        # View my task
        elif menu == "vm":
            my_tasks = task.view_mine(task.get_task(), current_user)
            option = input("Enter the task number to choose a task or '-1' to return to the main menu: ")
            if not (option == "-1"):
                for i in range(my_tasks):
                    if i == (int(option)-1):
                        sub_option = input("Enter 'm' to mark the task as completed or 'e' to edit the task: ")

                        # Mark the task as completed and update its value to "Yes"
                        if sub_option == 'm':
                            tasks[i]['completed'] = "Yes"
                            task_file._write("\n".join(task.process_task(tasks)))
                            print("Mark the task as completed successfully!")
                        
                        # Edit the task and update its due date as today
                        elif sub_option == 'e':
                            if tasks[i]['completed'] == "No":
                                tasks[i]['due_date'] = date.today()
                                task_file._write("\n".join(task.process_task(tasks)))
                                print("Task update successfully!")
                            else:
                                menu
            else:
                menu

        # Generate reports
        elif menu == "gr":

            # Generate a task overview report
            task_overview = task.task_overview(task.get_task())

            # Write the task overview report to the file
            task_overview_file = File("task_overview.txt")
            task_overview_file.create(task_overview)
            task_overview_file._write(task_overview)

            print()

            # Generate an user overview report
            user_overview = user.user_overview(task.get_task())

            # Write the user overview report to the file
            # user_overview_file = File("user_overview.txt")
           
            # user_overview_file.create(user_overview)
            
            # user_overview_file._write(user_overview)
           

        # Display statistics about number of users and tasks to admin user          
        elif menu == "ds":
            if current_user == "admin":
                print(f"\n")
                print("Statistics")
                print("-----------------------------------")
                print(f"Number of users: \t\t {len(user.get_user().keys())}")
                print(f"Number of tasks: \t\t {len(tasks)}")
                print("-----------------------------------") 

        # Exit the program   
        elif menu == "ex":
            print(f"{'-'*15}")
            print('Goodbye!!!')
            print(f"{'-'*15}")
            exit()
        
        # Invalid input
        else:
            print("You have made a wrong choice. Please try again!")