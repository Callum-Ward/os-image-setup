import json
import os
import subprocess

def install_packages(packages):
    subprocess.run(["apt-get", "update"])
    subprocess.run(["apt-get", "install", "-y"] + packages)

def remove_packages(packages):
    subprocess.run(["apt-get", "remove", "-y"] + packages)

def copy_files(src, dest):
    subprocess.run(["cp", "-r", src, dest])

def remove_files(files):
    for file in files:
        os.remove(file)

def edit_file(file, old_string, new_string):
    with open(file, "r") as f:
        contents = f.read()
    contents = contents.replace(old_string, new_string)
    with open(file, "w") as f:
        f.write(contents)

def resize_partition(partition, size):
    subprocess.run(["resize2fs", partition, size])

def insert_encrypted_partition(partition, keyfile):
    subprocess.run(["cryptsetup", "luksFormat", partition, keyfile])
    subprocess.run(["cryptsetup", "open", partition, "encrypted_partition"])
    subprocess.run(["mkfs.ext4", "/dev/mapper/encrypted_partition"])

def add_user(username):
    subprocess.run(["useradd", "-m", username])

def reconfigure_user(username, new_password):
    subprocess.run(["usermod", "-p", new_password, username])

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    os_image = config["os_image"]
    tasks = config["tasks"]

    for task in tasks:
        if task["type"] == "install_packages":
            install_packages(task["packages"])
        elif task["type"] == "remove_packages":
            remove_packages(task["packages"])
        elif task["type"] == "copy_files":
            copy_files(task["src"], task["dest"])
        elif task["type"] == "remove_files":
            remove_files(task["files"])
        elif task["type"] == "edit_file":
            edit_file(task["file"], task["old_string"], task["new_string"])
        elif task["type"] == "resize_partition":
            resize_partition(task["partition"], task["size"])
        elif task["type"] == "insert_encrypted_partition":
            insert_encrypted_partition(task["partition"], task["keyfile"])
        elif task["type"] == "add_user":
            add_user(task["username"])
        elif task["type"] == "reconfigure_user":
            reconfigure_user(task["username"], task["new_password"])
