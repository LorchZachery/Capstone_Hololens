import os, glob
import requests
import shutil
import json
import add_json as data
import stack_images as stack
from getmac import get_mac_address as gma


#baseURL to server
baseURL = 'http://10.1.100.138'

#where the bombs are
bombsCoor = [(39.0338362,-104.8850707),(39.0337238,-104.8842394)]

doneNames = []
def get_direcetory():
    ''''
    this function downloads a json of the file system that is on the sever so the correct files can be accessed
    '''
    #tells teh driectory.php script to make the json and what it should look like
    url = baseURL + '/scripts/directory.php'
    data = {'dir': '../', 'outfile': 'directory.json', 'options' : 'JSON_PRETTY_PRINT'}
    r = requests.post(url,data = data)
    
    #pulling the json that was jsut created
    directory = baseURL + '/scripts/directory.json'
    filename = directory.split("/")[-1]
    r = requests.get(directory, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
        
        print('json download: ',filename)
        with open(filename) as json_file:
            dir_json = json.load(json_file)
        print(json.dumps(dir_json, indent =4))
    else:
        print('json fail')

def getFiles():
    filename = 'directory.json'
    with open(filename) as json_file:
        dir_json = json.load(json_file)
    sets = dir_json["uploads"]
    return sets

def get_metadata_file():
    url = baseURL + '/uploads/metadata.json'
    filename = url.split("/")[-1]
    
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
        
        print('metadata updated')
        with open(filename) as json_file:
            dir_json = json.load(json_file)
        #print(json.dumps(dir_json, indent = 4))
        os.rename(filename, 'stacked/' + filename)

def check_metadata():
    in_meta = []
    filename = 'stacked/metadata.json'
    with open(filename) as json_file:
        dir_json = json.load(json_file)
    for image in dir_json["images"]:
        in_meta.append(image["image_name"])
    return in_meta

def pull_image(url):
    '''
    pull_image pulls the file at the given url and saves it to the localhost
    then places it in the data folder on localhost
    '''
    filename = url.split("/")[-1]
    r = requests.get(url, stream = True)
    
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
            
        
        print('image download: ',filename)
        os.rename(filename, '../data/' + filename)
    
    else:
        print("image failed")
        print(r.status_code)
    return
    
def find_url(baseNames):
    #opening directpry json
    filename = 'directory.json'
    with open(filename) as json_file:
        dir_json = json.load(json_file)
    
    #getting down to each file on the server
    sets = dir_json["files"]
    for sety in sets:
        batches = dir_json["files"][sety]
        for batch in batches:
            files = dir_json["files"][sety][batch]
            for file in files:
                testName = file.split('_')[0] + '_' + file.split('_')[1] + '_'
                if testName in baseNames and testName not in doneNames:
                    doneNames.append(testName)
                    image = testName + '3' + '.tif'
                    print(image)
                    url = baseURL + '/' + "files" + '/' + sety + '/' + batch + '/' + image
                    print(url)
                    pull_image(url)
                    print("adding to json")
                    data.createJson(image, bombsCoor)
                    


def post_metadata():
    '''
    this function post the meteadata.json
    '''
    print('posting metadata')
    file= 'stacked/metadata.json'
    url = baseURL + '/scripts/upload.php'
    data = {'type': 1, 'fileName': 'metadata.json', 'fileToUpload': open(file, 'rb').read()}
    r = requests.post(url, data = data)
    print(r.status_code)
    return
                   
if __name__ == "__main__":
    post_metadata()
    
    
    
    