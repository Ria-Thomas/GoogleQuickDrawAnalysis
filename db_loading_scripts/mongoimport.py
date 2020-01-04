#
# This code is written to populate the data into mongodb
# Code makes use of the available mongoimport cmd line utility to load the data
# 
#
#
# History of the file
#*********************
#
# Nov 2 2019 - creation - asundarr
# Nov 17 2019 - adding the changes to load the mongodb in VM - asundarr
# Dec 05 2019 - code revisited to change the dataset path - asundarr
#

import os 
import subprocess

path="/home/ubuntu/dataset/quickdraw_simplified/"

for f in os.listdir(path): 
    filename = os.path.join(path, f) 
    print(filename)
    subprocess.run(["mongoimport", "--db", "BigDataTrio", "--collection", "QuickDrawData", "--file", filename])
