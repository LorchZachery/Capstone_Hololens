import os
import requests
import shutil
import json

baseURL = 'http://96.66.89.62'
def post_image():
    #post image
    
    url = 'http://96.66.89.62/scripts/upload.php'
    data = {'type': 1, 'fileName': 'test.tif', 'fileToUpload': open('test.tif', 'rb').read()}
    r = requests.post(url, data = data)
    print(r.content)
    print("done upload")

def pull_image(url):
    #pull image
    #url = 'http://96.66.89.62/scripts/directory.php'
    #url = 'http://96.66.89.62/files/0017SET/000/IMG_0111_2.tif'
    filename = url.split("/")[-1]
    r = requests.get(url, stream = True)
    
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
            
        
        print('image download: ',filename)
    
    else:
        print("image failed")
    return

def get_direcetory():
    url = 'http://96.66.89.62/scripts/directory.php'
    data = {'dir': '../', 'outfile': 'directory.json', 'options' : 'JSON_PRETTY_PRINT'}
    r = requests.post(url,data = data)
    
    directory = 'http://96.66.89.62/scripts/directory.json'
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

def find_next_tif():
    filename = 'directory.json'
    with open(filename) as json_file:
        dir_json = json.load(json_file)
    stacked_images = dir_json["uploads"]
    sets = dir_json["files"]
    for set in sets:
        batches = dir_json["files"][set]
        for batch in batches:
            files = dir_json["files"][set][batch]
            for file in files:
                baseName = file.split('_')[0] + '_' + file.split('_')[1] + '_'
                if check_uploads(baseName):
                    for band in range(1,7):
                        image = baseName + str(band) + '.tif'
                        url = baseURL + '/' + "files" + '/' + set + '/' + batch + '/' + image
                        print(url)
                        pull_image(url)
                        
def check_uploads(baseName):
    stacked = baseName + 'stacked.tif'
    url = baseURL + '/uploads/' + stacked
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        print(baseName + ' already stacked')
        return False
    else:
        print('pulling ' + baseName + ' to be stacked')
        return True
    
    
   
if __name__ == '__main__':
     #pull_image()
     find_next_tif()