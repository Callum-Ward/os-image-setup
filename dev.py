import json
import sys
import subprocess
import os
import logging


def run_command(command, logging, display_output):

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)    
    except subprocess.CalledProcessError as e:
        # Handle the error
        print(e.stderr)
        logging.error(f" Program return code: {e.returncode}\n{e.stderr}")
        sys.exit(1)
        
    if result.returncode:
        if display_output: print(f"'{command}' FAILED")
        logging.error(f" command '{command}' return code: {result.returncode}\n{result.stderr}")
    else:
        if display_output: print(f"'{command}' EXECUTED")
        logging.info(f" command '{command}' returned: \n{result.stdout}")
    

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

    diplay_output = input("Display command output? (y/n): ").lower()
    if diplay_output == 'y':
        run_command(command, logging, True)
    else:
        run_command(command, logging, False)
        




