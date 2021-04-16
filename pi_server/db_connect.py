import os
import requests
import shutil
import json
import sys
import time



class db_connect(object):
    '''
    this allows you to connect to the database and insert lat and lons, good for debugging
    
    '''
    def __init__(self):
        self.dfcsURL = 'https://ied.dfcs-cloud.net/scripts/'
        self.url = self.dfcsURL + 'query.php'

    # SELECT is to select data, EDIT is for insert remove delete

    def query_db(self, statement, command, verbose=False):
        data = {'query': statement, 'type': command}
        # try:
        r = requests.post(self.url, data=data)
        # except:
        #    url = urlNetwork + 'scripts/query.php'
        #    r = requests.post(url, data = data)
        b = r.content.decode()
        
        if command == 'SELECT':
            load = json.loads(b)
            final = json.dumps(load, indent=4)
            if verbose:
                print(final)
            return load
        else:
            if verbose:
                print(b)
            return b

    def insert_latlon(self, lat, lon, last_id=False):
        new = False
        if last_id is False:
            new = True

        if new:
            select = 'SELECT ID from bombs'
            json_file = self.query_db(select, 'SELECT')
            last_id = -1
            for i in range(0, len(json_file)):
                last_id = json_file[i]["ID"]
            last_id = str(int(last_id) + 1)
            insert = 'INSERT INTO bombs (ID, lat, lon) VALUES (' + last_id + ', ' + str(lat) + ',' + str(lon) + ')'
        else:
            insert = 'UPDATE bombs SET lat = ' + str(lat) + ', lon= ' + str(lon) + 'WHERE ID = ' + str(last_id)

        result = self.query_db(insert, 'EDIT')
        if not result:
            print("query failed")
        elif new:
            print('new bomb created with ID: ' + str(last_id) + ' with lat: ' + str(lat) + ' lon: ' + str(lon))
        else:
            print('bomb ' + str(last_id) + ' was updated with lat: ' + str(lat) + ' lon: ' + str(lon))

    def check_db(self, table):
        select = 'SELECT * from ' + table
        self.query_db(select, 'SELECT', True)

    def delete(self, id):
        delete = 'DELETE FROM bombs WHERE ID=' + str(id)
        self.query_db(delete, 'EDIT')

    def updateXY(self, curr_lat, curr_lon):
        url = self.dfcsURL + 'x_y.php'

        data = {'lat': curr_lat, 'lon': curr_lon}
        try:
            r = requests.post(url, data=data)
        except:
            r = requests.post(url, data=data)

        b = r.content.decode()
        print(b)

    #
    # updateXY(0,0)
    # insert_latlon(39.00863265991211,-104.88196563720703)
    # updateXY(39.008431, -104.883484)

    # statement = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_SCHEMA='bomb_location'"
    def check(self, verbose=False):
        statement = 'SELECT * from bombs'
        return self.query_db(statement, 'SELECT', verbose)