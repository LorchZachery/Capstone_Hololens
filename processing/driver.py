import os, glob
import requests
import shutil
import json
import add_json as data
import stack_images as stack

#baseURL to server
baseURL = 'http://10.1.100.138'

#where the bombs are
bombsCoor = [(39.0338362,-104.8850707),(39.0337238,-104.8842394)]

errorFiles = []
def post_image(image):
    ''''
    post_image sends an image to the sever using the upload.php script
    type 1 puts the image in the uploads folder
    type 2 puts the image in the scripts folder (good for changing scripts from away from server)
    type 3 puts the image in the root folder (good fro html edits)
    '''
    # this is where the stacked image is on localhost
    print('posting: ' + image)
    file= 'stacked/'+ image
    url = baseURL + '/scripts/upload.php'
    #uploading image
    data = {'type': 1, 'fileName': image, 'fileToUpload': open(file, 'rb').read()}
    r = requests.post(url, data = data)
    print(r.content)
    print("done upload")

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

def driver():
    '''
    main driver code for the pulling 6 bands of an image, then stacking them, updating the metajson data
    then push the stacked image and metadata back to the server
    '''
    #opening directpry json
    filename = 'directory.json'
    with open(filename) as json_file:
        dir_json = json.load(json_file)
    
    #getting down to each file on the server
    sets = dir_json["files"]
    for set in sets:
        batches = dir_json["files"][set]
        for batch in batches:
            files = dir_json["files"][set][batch]
            for file in files:
                #baseName is the file name without its band number
                baseName = file.split('_')[0] + '_' + file.split('_')[1] + '_'
                
                # checking if the file has already been stacked
                if check_uploads(baseName):
                    #getting each band for the image
                    for band in range(1,7):
                        image = baseName + str(band) + '.tif'
                        url = baseURL + '/' + "files" + '/' + set + '/' + batch + '/' + image
                        print(url)
                        #pullling the image band
                        pull_image(url)
                    
                    #giving the images to stack function
                    image_wild = baseName + '*.tif'
                    imagePath = os.path.join('..','data')
                    imageNames = glob.glob(os.path.join(imagePath,image_wild))
                    successCode = stack.stackImages(baseName, imageNames)
                    if successCode != -1:
                        #updating the metadata json
                        update_metadata(baseName)
                        
                        #update errorFiles.txt
                        update_errorFiles()
                        
                        #pushing the image and metadata
                        post_metadata()
                        post_image(baseName + 'stacked.tiff')
                        
                        #deleting stacked image
                        stacked = '../processing/stacked/' + baseName + 'stacked.tiff'
                        os.remove(stacked)
                    else:
                        #error handling
                        print(baseName + ' skipped due to stacking errors')
                        #adding file to errorFile.txt
                        post_errorFiles(baseName)
                    
                    #deleting the bands
                    delete_images(image_wild)
                    
def check_uploads(baseName):
    '''
    this function checks if the file is already stacked and on the server
    '''
    with open('errorFiles.txt') as f:
        if baseName in f.read():
            return False
    stacked = baseName + 'stacked.tiff'
    url = baseURL + '/uploads/' + stacked
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        print(baseName + ' already stacked')
        return False
    else:
        print('pulling ' + baseName + ' to be stacked')
        return True

def update_metadata(baseName):
    '''
    this function pulls the current metadata json and then updataes it with new data
    '''
    url = baseURL+ '/uploads/metadata.json'
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
    else:
        print('metadata update failed')
    
    #using file for band three just as the base file to get over arching meta data
    file = baseName + '3.tif'
    data.createJson(file, bombsCoor)

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
    
def update_errorFiles():
    '''
    updates a txt file of files that have filed
    '''
    url = baseURL+ '/uploads/errorFiles.txt'
    filename = url.split("/")[-1]
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(filename, "wb") as f:
            shutil.copyfileobj(r.raw,f)
        
        print('errorFiles updated')
        os.rename(filename,  filename)
    else:
        print('errorFiles update failed')

def post_errorFiles(baseName):
    '''
    adds failed file to errorFiles.txt and uploads to server
    '''
    file = open("errorFiles.txt","w")
    file.write(baseName)
    file.write("\n")
    file.close()
    
    print('posting errorFiles')
    file= 'errorFiles.txt'
    url = baseURL + '/scripts/upload.php'
    data = {'type': 1, 'fileName': 'errorFiles.txt', 'fileToUpload': open(file, 'rb').read()}
    r = requests.post(url, data = data)
    print(r.status_code)
    return
    
    
    
def delete_images(image_wild):
    '''
    deletes images in the wild card set
    '''
    files = glob.glob('../data/' + image_wild)
    for file in files:
        os.remove(file)
    print("bands delted")
    
    
    
   
if __name__ == '__main__':
     get_direcetory()
     driver()