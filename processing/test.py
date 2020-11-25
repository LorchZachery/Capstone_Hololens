import dp_connect as db
from getmac import get_mac_address as gma
baseName =  "test1"
MAC = gma()
#print(MAC)
#statement = "INSERT INTO  currentfiles (BaseName, MAC) VALUES(" + "'"+  baseName  + "','" + gma() + "' )"
#statement = "SELECT max(image_id) from images"

image_id = -1
image_name = "test"
yaw =-2
pitch = -3
roll = -4
height = -5
#statement = "INSERT INTO  images (image_id, image_name, yaw, pitch, roll, height) VALUES(" + str(image_id) + ", '"+  image_name  + "', " + str(yaw) + "," + str(pitch) + "," + str(roll) +  "," + str(height) + ")"

"""
"INSERT INTO gps (id, area, lat, lon) VALUES (" + str(image_id) +", 'center'," 


print(statement)
result = db.query_db (statement, 'EDIT', True)
print(result)
"""
statement = "SELECT * from currentfiles where BaseName=" + "'" +  baseName + "'"
print(statement)
result = db.query_db(statement, 'SELECT', True)
print(result)
if(len(result) != 0):
	print(baseName + " being stacked by another machine")
