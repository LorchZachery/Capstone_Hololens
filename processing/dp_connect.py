import os 
import requests
import shutil
import json
import sys

urlInternet = 'http://96.66.89.62/' 
urlNetwork = 'http://10.1.100.138/scripts/query.php'
dfcsURL = 'https://ied.dfcs-cloud.net/'
url = urlNetwork #dfcsURL + 'scripts/query.php'

#SELECT is to select data, EDIT is for insert remove delete


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
    url = dfcsURL + "scripts/x_y.php"
    data = {'lat' : curr_lat , 'lon' : curr_lon }
    try:
        r = requests.post(url, data = data)
    except:
        url = urlNetwork + 'scripts/x_y.php'
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

#insert into current working files
#statement = "INSERT INTO currentfiles (BaseName, MAC) VALUES  ('test', '1234')"
#query_db(statement, 'EDIT', True)
#check()



#statement = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'errorfiles'"
#query_db(statement, 'SELECT', True)
#updateXY()
#insert_latlon(39.009056, -104.882127)
#insert_latlon(39.008894,-104.881702)
#insert_latlon(39.009060, -104.881286)
#insert_latlon(39.009185, -104.881704)
#insert_latlon(39.009188, -104.881702)
#updateXY(39.009264, -104.881704)
#insert_latlon(39.009264, -104.881704)
#insert_latlon(39.009273, -104.881727)
#insert_latlon(39.009276, -104.881674)
#insert_latlon(39.009234, -104.881677)




#check_db('bombs')
