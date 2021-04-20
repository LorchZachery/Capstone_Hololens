#########################################################################################################
# Author - C1C Jonathan Nash, @JonathanNash21
# Last Updated - 17 Mar 2021
# Brief - Main function that will use a given folder of images and send them one at a time to the AI to 
# 		  parse through. Also runs database functions once all the images have been processed (can be 
#  		  updated to run asynchronously when each new "bomb" has been found).
#########################################################################################################
from obj_det_custom_yolo_live import Adjusted
from init import Init
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
dfcsURL = 'http://10.10.10.40/capstone/scripts/'
url = dfcsURL + 'query.php'

#initialize main dictionary, important variables, etc. -> init.py
initial = Init()

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
#imgset = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\test_images'

# print(os.listdir(imgset))
# initialize the Adjusted class -> obj_det_custom_yolo_live.py
adj = Adjusted()

if initial.access_path: # not doing the hardcoded test
	try: # allows for a keyboard interrupt
		while(True): # continuously run this code until a keyboard interrupt occurs
			update = 0 # check to see if the AI ran
			if initial.mutex == 1: # check to see if init can access the files
				#print("in mutex 1")
				asyncio.run(initial.look_for_image()) # look for images in the unaccessed folder -> init.py/look_for_image
			if len(initial.queue) > 0:# and initial.mutex == 2: # if there are images to run and AI can access the files
				#print("in mutex 2")
				adj.AIRun(initial.queue[0]) # run the AI on the first image in the queue -> obj_det_custom_yolo_live.py
				#adj.AIRun() # testing purposes only
				initial.queue.pop(0) # remove the image we just ran through the AI
				initial.mutex = 1 # change locks
				update = 1 # make it so we don't try to update the database every time if there is nothing new to add
			if update:
				img_data = initial.get_img_data() # get the updated data
				
				for img in img_data: # for each image in the dictionary, send any new data to the database
					# print(img)
					# the second dictionary has entries separated by bounding box (x, y) coordinates (coordinates in reference to image size, not GPS)
					for box in img_data[img]: # for each bounding box in the image
						#print("box")
						# limit entries sent to database to 5, for testing purposes only (everything will work without this, this is only used for proof of concept)
						#if i > 5:
						#	break
						# there is other information stored in the initial dictionary that is not the second dictionary, we want to skip over this
						#print(type(init.img_data[img][box]))
						#print(init.img_data[img][box])
						if type(img_data[img][box]) is not dict or initial.img_data[img][box]["database_update"] == 1: # make sure we are accessing the correct data, and only that which was newly added
							continue
						# insert the appropriate information into the database	
						#insert_latlon(initial.img_data[img][box]['lat'], initial.img_data[img][box]['lon']) # sometimes commented out so we don't get runtime errors due to not being connected to db
						initial.img_data[img][box]["database_update"] = 1 # mark this data as having already been sent to the database
						
						#i += 1 # counter to limit entries to database, if desired
						#print("lat:" + str(init.img_data[img][box]['lat']) + ", lon: " + str(init.img_data[img][box]['lon']))
			time.sleep(5) # sleep for 5 seconds before checking everything again, general use should be longer
	except KeyboardInterrupt: # if ctrl+c is hit, stop the program
			print("Exiting while loop")
			pass
else: # testing only, nothing in unaccessed folder
	#adj.AIRun("D:\HololensIED\CapstoneAI\loctets.jpeg") #for testing the whole shindig - should run this using the unaccessed folder now
	adj.AIRun() # will run AIRun with the filename == None, which just goes to a default image value

