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
dfcsURL = 'http://192.168.1.135/capstone/scripts/'
url = dfcsURL + 'query.php'
#from dp_connect import Update

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

def insert_latlon(lat, lon, last_id=False):
    new = False
    if last_id is False:
        new = True
    
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


#statement = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='bomb_location'"
def check():
    statement = 'SELECT * from currentfiles'
    query_db(statement, 'SELECT', True)


imgset = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\test_images'

# print(os.listdir(imgset))
adj = Adjusted()
"""
for img in os.listdir(imgset):
    img = imgset + "\\" + img
    # print(img)
    
    adj.testRun(img)
"""
#asyncio.run(Catch)
adj.testRun()
print("finished test run")
print(init.img_data)
i = 0
for img in init.img_data:
	print(img)
	for box in init.img_data[img]:
		if i > 5:
			break
		if type(init.img_data[img][box]) is not dict:
			continue
		insert_latlon(init.img_data[img][box]['lat'], init.img_data[img][box]['lon'])
		i += 1
		#print("lat:" + str(init.img_data[img][box]['lat']) + ", lon: " + str(init.img_data[img][box]['lon']))
		
