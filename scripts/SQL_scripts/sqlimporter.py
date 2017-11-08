import os
from pathlib import Path
from shutil import copyfile
from subprocess import check_output
from time import sleep

USERNAME = "root"
PASSWORD = "root"
DATABASE = "steam"
DIR_PATH = "E:/pratik/steam_data"
MYSQLPATH = "C:/Program Files/MySQL/MySQL Server 5.7/bin/"
DESKTOP = "C:/Users/Pratik Anand/Desktop"
cmd = "mysql -f -u {} -p{} {}".format(USERNAME, PASSWORD, DATABASE)
PAUSE_FILE = "C:/Users/Pratik Anand/Desktop/0"

os.chdir(DIR_PATH)
file_list = os.listdir()


sorted_file_list = sorted(file_list, key=lambda y: int(y.split("-")[0]))
# print(sorted_file_list)
skip = 166336
os.chdir(MYSQLPATH)
for filename in sorted_file_list :
    if skip >= int(filename.split('-')[0]) :
        print("Skipping ", filename)
        continue

    while True :   #to pause the processing in between movements
        my_file = Path(PAUSE_FILE)
        if my_file.is_file():
            print("Sleeping as 0 file exists at ", PAUSE_FILE )
            sleep(1)
        else :
            break
    # print("Copying file ", filename)
    # copyfile(DIR_PATH+ "/" +filename, DESKTOP + "/" + filename)
    print("Processing ", filename)
    new_cmd = cmd + ' < "{}"'.format( DIR_PATH+ "/" +filename)
    print(check_output(new_cmd, shell=True))
    # os.remove(DESKTOP + "/" + filename)
