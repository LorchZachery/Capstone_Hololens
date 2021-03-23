#########################################################################################################
# Author - C1C Jonathan Nash, @JonathanNash21
# Last Updated - 17 Mar 2021
# Brief - Main function that will use a given folder of images and send them one at a time to the AI to 
# 		  parse through. Also runs database functions once all the images have been processed (can be 
#  		  updated to run asynchronously when each new "bomb" has been found).
#########################################################################################################
from obj_det_custom_yolo_live import Adjusted
import os
import init
from asynchronous import Catch
import asyncio
import os 
import requests
import shutil
import json
import sys
import time
from image_data import ImageData

# current database location, ran by C1C Zach Lorch (@LorchZachery)
dfcsURL = 'http://10.10.10.2/capstone/scripts/'
url = dfcsURL + 'query.php'


#print(init.x)

def query_db(statement, command, verbose=False):
    data = {'query' : statement, 'type' : command}
    #try:
    r = requests.post(url, data = data)
    #except:
    #    url = urlNetwork + 'scripts/query.php'
    #    r = requests.post(url, data = data)
    b = r.content.decode()
    if command == 'SELECT':
        load = json.loads(b)
        final = json.dumps(load, indent =4)
        if verbose:
            print(final)
        return load
    else:
        if verbose:
            print(b)
        return b

# insert the lat and lon of a found bomb to the database
def insert_latlon(lat, lon, last_id=False):
    new = False
    if last_id is False:
        new = True
    #print("hit me")
    if new:
        select = 'SELECT ID from bombs' 
        json_file = query_db(select, 'SELECT')
        last_id = -1
        for i in range(0, len(json_file)):
            last_id = json_file[i]["ID"]
        last_id = str(int(last_id) + 1)
        insert = 'INSERT INTO bombs (ID, lat, lon) VALUES (' + last_id + ', '+ str(lat) +',' + str(lon) + ')'
    else:
        insert = 'UPDATE bombs SET lat = ' + str(lat) + ', lon= '+ str(lon) + 'WHERE ID = ' + str(last_id)
    
    result = query_db(insert, 'EDIT')
    if not result:
        print("query failed")
    elif new:
        print('new bomb created with ID: ' + str(last_id) + ' with lat: ' + str(lat) + ' lon: ' + str(lon))
    else:
        print('bomb ' + str(last_id) + ' was updated with lat: ' + str(lat) + ' lon: ' + str(lon))
'''
def check_db(table):
    select = 'SELECT * from ' + table
    query_db(select, 'SELECT', True)

def delete(id):
    delete = 'DELETE FROM bombs WHERE ID=' + str(id)
    query_db(delete,'EDIT')

def updateXY(curr_lat, curr_lon):
    url = dfcsURL + 'x_y.php'

    data = {'lat' : curr_lat , 'lon' : curr_lon }
    try:
        r = requests.post(url, data = data)
    except:
        r = requests.post(url, data = data)

    b = r.content.decode()
    print(b)

#
#updateXY(0,0)
#insert_latlon(39.00863265991211,-104.88196563720703)
#updateXY(39.008431, -104.883484)


def check():
    statement = 'SELECT * from currentfiles'
    query_db(statement, 'SELECT', True)

'''
# the file location for image files I want to run through the AI
imgset = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\test_images'

# print(os.listdir(imgset))
# initialize the Adjusted class
adj = Adjusted()

# run each image through the AI
'''for img in os.listdir(imgset):
    img = imgset + "\\" + img
    # print(img)
    image_info = image_data.ImageData(img)
    adj.AIRun(img)
'''
#asyncio.run(Catch)
#image_info = ImageData("test_images/1.jpg")
adj.AIRun() # will run AIRun with the filename == None, which just goes to a default image value
#print("finished AI run")
#print(init.img_data)

i = 0
# send each found bomb to the database
# each bomb is held in a dictionary{dictionary} structure, where the initial dictionary has entries separated by image name
for img in init.img_data:

	print(img)
	# the second dictionary has entries separated by bounding box (x, y) coordinates (coordinates in reference to image size, not GPS)
	for box in init.img_data[img]:
		#print("box")
		# limit entries sent to database to 5, for testing purposes only (everything will work without this, this is only used for proof of concept)
		#if i > 5:
		#	break
		# there is other information stored in the initial dictionary that is not the second dictionary, we want to skip over this
		#print(type(init.img_data[img][box]))
		#print(init.img_data[img][box])
		if type(init.img_data[img][box]) is not dict:
			continue
		# insert the appropriate information into the database	
		#print("cont")
		insert_latlon(init.img_data[img][box]['lat'], init.img_data[img][box]['lon'])
		
		i += 1
		#print("lat:" + str(init.img_data[img][box]['lat']) + ", lon: " + str(init.img_data[img][box]['lon']))
		
#imgData = ImageMetaData("D:\HololensIED\CapstoneAI\loctets.jpeg")
