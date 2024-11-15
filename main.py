from concurrent.futures import ThreadPoolExecutor
import threading
from time import sleep
from colorama import Fore, Style, init
import questionary
import sys
import os
import subprocess
import pygetwindow as gw
import filelock
import manage_csv
import thread_main

# Set main directory path
MAIN_DIR = r"D:\EDIT VIDEO"


# Check if directory exists, exit if not found
if not os.path.exists(MAIN_DIR):
    print("Directory not found!")
    exit(1)

# Initialize a lock for the critical section
lock = threading.Lock()

CSV_FILE_NAME = 'urls.csv'
current_dir = os.getcwd()
# Navigate to the parent directory
csv_file_path = os.path.join(current_dir, CSV_FILE_NAME)

_csv_file_lock_path = os.path.join(current_dir, 'csv.lock')
_csv_file_lock = filelock.FileLock(_csv_file_lock_path)


def run_command(cmd, directory):
    process = subprocess.Popen(cmd, shell=True, cwd=directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.pid

def run_command_1(command):
    """Run an ADB command using subprocess."""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}\n{stderr.decode('utf-8')}")
    # else:
    #     print(f"Successfully ran command: {command}")
    return stdout.decode('utf-8')


def concurrent_run_instances(thread_count, profiles):
    def perform_task(profile):
        print(profile)
        while True:
            with lock:  # Wait up to 10 seconds to acquire the lock:
                try:
                    folder_name, yt_link = manage_csv.get_folder_and_link()
                except Exception as e:
                    print(Fore.RED + f"ERROR: {str(e)} No link to use in " + Style.RESET_ALL, CSV_FILE_NAME)
            
            result = thread_main.run_thread(MAIN_DIR, folder_name, yt_link, profile)
            print(result)
            with lock:
                manage_csv.update_cell(folder_name)

        

    # with ThreadPoolExecutor(max_workers=thread_count) as executor:
    #     for _ in range(thread_count):
    #         executor.submit(perform_task)
    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        executor.map(perform_task, profiles)

firefox_profiles = [
    "7njcb218.jonyhendritiga@gmail.com",
    "dbmn7v7e.kasiankak09@gmail.com",
    "g2tscum7.mapanjackpot@gmail.com",
    "kfieaus2.dewadora13@gmail.com",
    "kgn17ku9.putriduyung28xxx@gmail.com",
    "lnjnuk8y.yoyotheyoyoking@gmail.com",
    "m3a0w4c4.bambobambi196@gmail.com",
    "r6q53axy.putrifiona518@gmail.com",
    "r8bcqoi8.prakosoheng@gmail.com",
    "xhr55g3n.mapan77.official@gmail.com",
    ]

# Initialize colorama
init()

thread_number = int(input(Fore.BLUE + "Please enter a number of thread: " + Style.RESET_ALL))
print(Fore.GREEN + "You entered the number:" + Style.RESET_ALL, thread_number)


firefox_profiles = firefox_profiles[:thread_number]


concurrent_run_instances(thread_number, firefox_profiles)