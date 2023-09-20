import json
import sys
import subprocess

def run_command(command, display_output=False):
    if display_output:
        result = subprocess.run(command, capture_output=True, text=True)
        print(result.stdout)
    else:   
        subprocess.run(command)


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
    
    # Example usage
    command = input("Enter a command: ").split()

    diplay_output = input("Display command output? (y/n): ")
    if diplay_output == 'y':
        run_command(command, True)
    else:
        run_command(command)
        




