import json
import sys
import subprocess


if __name__ == "__main__":

    # Parse command-line arguments
    config_file = sys.argv[1]

    # Load config file
    with open(config_file) as f:
        config = json.load(f)

    name = 'name' in config['os_image'] ? config['os_image']['name'] : config['os_image']['link']

    # Check if a name is used
    if 'name' in config['os_image']:
        name = config['os_image']['name']
        print(f"os_image: {name}")
    



