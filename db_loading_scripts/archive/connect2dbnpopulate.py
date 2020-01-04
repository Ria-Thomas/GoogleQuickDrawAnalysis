#
# This file is the first of the files written to populate the data into mongodb
# Requires a relook at the way we do it
# 
#

#
# History of the file
#*********************
#
# Nov 2 2019 - creation - asundarr
#

import os
import json
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.mydb

def read_data(path):
    for f in os.listdir(path):
        with open( os.path.join(path, f)) as logfile:
            for line in logfile:
                print(line)
                db.mycol.insert_one(line) 
    
 
if __name__ == '__main__':
    read_data("/home/abhishek/Desktop/test")
    count = db.mycol.count()
    print(count)
