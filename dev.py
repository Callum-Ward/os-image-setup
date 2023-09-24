import json
import sys
import subprocess
import os
import logging
from abc import ABC, abstractmethod

class TaskFactory:
    @staticmethod
    def create_task(task):
        print(f"create_task: {task['type']}")
        #create a switch statement instead of if/else
        task_mapping = {
            "install_packages": PackageInstall
        }
        TaskClass = task_mapping.get(task['type'], None)
        if TaskClass is None:
            pass
            #raise ValueError(f"Task type '{task['type']}' not supported")
        else:
            return TaskClass(task['type'], task['args'])


class TaskManager:
    def __init__(self,tasks,logging):
        self.tasks = []
        self._logging = logging
        for task in tasks:
            new_task = TaskFactory.create_task(task)
            if new_task is None:
                print(f"Task type '{task['type']}' not supported")
            else:
                self.tasks.append(TaskFactory.create_task(task))
        
    def _log(self, result):
        if result.returncode:
            logging.error(f" command '{command}' return code: {result.returncode}\n{result.stderr}")
        else:
            logging.info(f" command '{command}' returned: \n{result.stdout}")

    def _execute(self, task):
        task.state = "EXECUTING"
        result = None
        try:
            for command in task.commands:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                self._log(result)
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            logging.error(f" Program return code: {e.returncode}\n{e.stderr}")
            sys.exit(1)
        task.state = "DONE" if result.returncode == 0 else "CANCELLED"

    def run_tasks(self, display_output):
        for task in self.tasks:
            self._execute(task)
            if display_output: print(f"{task.name} task is: {task.state}")

class BaseTask(ABC):
    def __init__(self, name, args):
        self.name = name
        self.state = "PENDING"
        self.commands = self.set_commands(args)

    @abstractmethod
    def set_commands(self, args):
        pass

class PackageInstall(BaseTask):
    def set_commands(self, args):
        commands = ["ls"]
        package_names = args['packages']
        #commands = [f"apt-get install -y {package_names}"]
        return commands
    

if __name__ == "__main__":

    # Parse command-line arguments
    config_file = sys.argv[1]

    # Load config file
    with open(config_file) as f:
        config = json.load(f)

    # Check if a name is used
    if 'name' in config['os_image']:
        name = config['os_image']['name']
        print(f"os_image: {name}")
    else:
        print("No name provided for os_image")
        os._exit(1)

    logging.basicConfig(filename="command_log.txt", filemode="w", level=logging.INFO)

    command = input("Enter a command: ")

    output = input("Display command output? (y/n): ").lower()
    display_output = True if output == 'y' else False

    task_manager = TaskManager(config['tasks'],logging)
    task_manager.run_tasks(display_output)



    
        




