import os, glob
import add_json as data
import stack_images as stack
import json

def doneImages():
    meta_json = os.path.join("stacked", "test_data.json")
    with open(meta_json) as json_file:
        data = json.load(json_file)
        images = data["images"]
        image_names = []
        for image in images:
            name = image["image_name"].split(".")[0]
            image_names.append(name[:-7])
    return image_names
if __name__ == '__main__':
    bombsCoor = [(39.0338362,-104.8850707), (39.0337238 , -104.8842394)]
    
    
    index = 0
    imagePath = os.path.join('..','test_data')
    for file in os.listdir(imagePath):
        stripped_file = file.split(".")[0]
        FILE = stripped_file[:-1]
        if FILE not in doneImages():
            print("stacking: " + FILE)
            image_wild = FILE + '*.tif'
            imageNames = glob.glob(os.path.join(imagePath,image_wild))
            #panelNames = glob.glob(os.path.join(imagePath,'IMG_0111_*.tif'))
            
            stack.stackImages(FILE, imageNames)
            
            file = FILE + '3.tif'
            data.createJson(file, bombsCoor)
            index += 1
    print(str(index) + " images stacked")