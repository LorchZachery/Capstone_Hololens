
import requests
import shutil
import json
import os
import sys
baseURL = 'http://96.66.89.62/'

def get_metadata():
    ''''
    this function downloads a json of the file system that is on the sever so the correct files can be accessed
    '''
    #pulling the json that was jsut created
    directory = baseURL + 'uploads/metadata.json'
    filename = directory.split("/")[-1]
    r = requests.get(directory, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
        
        print('metea download: ',filename)
        with open(filename) as json_file:
            dir_json = json.load(json_file)
        print(json.dumps(dir_json, indent =4))
    else:
        print('json fail')
        
get_metadata()
