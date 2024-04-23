#!/bin/python3

from getpass import getpass
import subprocess

def get_archive_name(encrypted_file):
    archive_name = encrypted_file[:-4]
    return archive_name

def decrypt_archive(password, encrypted_file):
    archive_name = get_archive_name(encrypted_file)
    command = f"openssl enc -d -aes-256-cbc -iter 10000 -k {password} < {encrypted_file} > {archive_name}"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    return archive_name

def decompress_archive(archive_name):
    command = f"zstd -d --rm {archive_name}"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    archive_name = get_archive_name(archive_name)
    return archive_name

def extract_files(archive_name):
    command = f"tar -xf {archive_name}"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    command = f"rm {archive_name} {archive_name}.zst.enc"
    subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
 


# main
if __name__ == '__main__':
    full_backup_path = input("Inserisci il percorso del file di backup cifrato: ")
    password = getpass()

    print(f"Decrypting backup")
    zst_file = decrypt_archive(password, full_backup_path)

    print(f"Decompressing backup")
    tar_file = decompress_archive(zst_file)
    tmp = tar_file.split("/")
    tar_file = tmp[-1]

    print(f"Extracting backup")
    extract_files(tar_file)

    print("Extraction complete")