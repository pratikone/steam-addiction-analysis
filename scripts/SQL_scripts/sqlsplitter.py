###########################################################################################################
# Created by :
#  PRATIK ANAND
#  github.com/pratikone
# It splits a large SQL dump file into smaller files.
# It preservers queries by only splitting at ;
# It launches a new thread for write I/O operation
# Tested on SQL dump of size 170 GB
# It is resumable by filename as it creates filename with lines 
# For example, if a file contains lines from 501 - 2000 , the filename will be 500-2000
# Using this information, skip set to 2000 will start the script from line 2001 next time you launch it
# Timestamp : Nov 1 2017
############################################################################################################

#TODO : Keep size of file in consideration while splitting and find a better way to calculate that 
# as sys.getsizeof() doesn't provide accurate results

import threading

INPUT_FILE = "H:/steam.sql"

OUTPUT_FOLDER = "G:/steam_data"

CHUNK = 500   #lines
# SIZE_LIMIT_MB = 1024 * 1024
# SIZE_LIMIT = 1024   #bytes


def write_to_file(file_name, data_to_write) :
    print("Starting new thread to write to", file_name)
    with open(OUTPUT_FOLDER + "/" + file_name, "w", encoding="utf-8") as f:
        for item in data_to_write:
            f.write("%s\n" % item)

with open(INPUT_FILE, "r", encoding="utf-8") as fileobject:
    count = 0
    skip = 100203    #to avoid splitting already processed lines, change it to correct line number
    start_count = count
    chunk_check = count
    buffer_space = []
    for line in fileobject:
        count = count + 1
        if count <= skip :
            if count % 500 == 0 :
                print("Skipping till line ", count)
            start_count = count
            chunk_check = count
            continue
        # print("Processing line ", count)
        line = line.strip()
        buffer_space.append(line)
        if ";" in line and (count - chunk_check) > CHUNK :
            print("Processed till line {}".format(count))
            # if list_size > SIZE_LIMIT :
            file_name = "{}-{}".format(start_count, count)
            t = threading.Thread(target=write_to_file, args=(file_name, buffer_space[:]))
            # t.daemon = True
            t.start()
            buffer_space = []
            start_count = count
            chunk_check = count
            # else :
                #chunk_check = count

    #last part
    file_name = "{}-{}".format(start_count, count)
    t = threading.Thread(target=write_to_file, args=(file_name, buffer_space[:]))
    t.start()

print("DONE. Chalo Party karein")



