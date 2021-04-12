import mysql.connector
import json
from db_connect import db_connect
from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

print("EXECUTING script " + current_time)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="6yhn7ujm^YHN&UJM",
  database="capstone"
)


mycursor = mydb.cursor()


mycursor.execute("SELECT * FROM bombs")

localBombs = mycursor.fetchall()

bigDB = db_connect()
info = bigDB.check()

local_LatLons = []
net_LatLons = []
for i in range(0, len(localBombs)):
    lat = '%.6f'%(localBombs[i][1])
    lon = '%.6f'%(localBombs[i][2])
    local_LatLons.append((float(lat), float(lon)))


for i in range(0, len(info)):
    net_LatLons.append((float(info[i]["lat"]),float(info[i]["lon"])))


# adding from net database
mycursor.execute("SELECT MAX(ID) from bombs")
maxID = mycursor.fetchmany(size=1)[0][0]
if maxID is None:
    maxID = 0
else:
    maxID = maxID + 1

print("   checking local DB")
for x in range(0,len(net_LatLons)):
    if net_LatLons[x] not in local_LatLons:
        lat = net_LatLons[x][0]
        lon = net_LatLons[x][1]
        insert = 'INSERT INTO bombs (ID, lat, lon) VALUES (' + str(maxID) + ', ' + str(lat) + ',' + str(lon) + ')'
        print('new local bomb created with ID: ' + str(maxID) + ' with lat: ' + str(lat) + ' lon: ' + str(lon))
        mycursor.execute(insert)
        maxID +=1

mydb.commit()


## pushing up to net database
#
## remove redundancies from local
#
## adding new bombs to net database

print("   checking net DB")
for i in range(0, len(local_LatLons)):
    if local_LatLons[i] not in net_LatLons:
        bigDB.insert_latlon(local_LatLons[i][0], local_LatLons[i][1])



