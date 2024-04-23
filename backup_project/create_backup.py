#!/bin/python3

import os
import subprocess
from datetime import date

#global variables
today = date.today()
backup_name = "desktop_backup_" + today.strftime("%Y-%m-%d") + ".tar"

#functions
def find_useless_files():
    ini_lnk_files = []
    for file in os.listdir(desktop_path):
        if file.endswith(".ini") or file.endswith(".lnk"):
            file_path = desktop_path + "/" + file
            ini_lnk_files.append(file_path)
    return ini_lnk_files

def find_build_dirs():
    build_dirs = []
    for (root, dirs, _) in os.walk(desktop_path):
        for dir in dirs:
            if dir == "build":
                directory = os.path.join(root, dir)
                build_dirs.append(directory)
    return build_dirs

def create_file_exclude(ini_lnk_files, build_dirs):
    with open("exclude.txt", "w") as file:
        file.write(f"{desktop_path}/flutter\n")
        file.write(f"{desktop_path}/exclude.txt\n")
        file.write(f"{desktop_path}/{backup_name}\n")
        for f in ini_lnk_files:
            file.write(f"{f}\n")
        for d in build_dirs:
            file.write(f"{d}\n")

def create_archive():
    command = f"tar -cf {backup_name} --exclude-from=exclude.txt {desktop_path}"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

def compress_archive():
    command = f"zstd -z --rm -19 -T10 {desktop_path}/{backup_name} --quiet"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

def encrypt_archive():
    command = f"openssl enc -aes-256-cbc -salt -iter 10000 -k {password} < {desktop_path}/{backup_name}.zst > {desktop_path}/{backup_name}.zst.enc"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    command = f"rm {desktop_path}/{backup_name}.zst exclude.txt"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)



# main
if __name__ == '__main__':
    desktop_path = input("Inserisci il percorso della cartella Desktop: ")
    print("Inserisci la password: ")
    password = getpass()

    print("Finding files to exclude")
    ini_lnk_files = find_useless_files()
    build_dirs = find_build_dirs()

    create_file_exclude(ini_lnk_files, build_dirs)

    print("Creating the backup archive")
    create_archive()

    print("Compressing the archive")
    compress_archive()

    print("Encrypting the archive")
    encrypt_archive()

    print("Backup complete")
