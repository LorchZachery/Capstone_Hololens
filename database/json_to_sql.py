import json

filename = 'metadata.json'

with open(filename) as json_file:
    file = json.load(json_file)
    metadata = file[0]

keys = metadata.keys()
key_list = []
  


for key in keys:
    try:
        subkeys = metadata[key][0].keys()
        subkeys_list =[]
        for subkey in subkeys:
            subkeys_list.append(subkey)
        key_list.append((key,subkeys_list))
    except:
        key_list.append((key, []))

# INSERT INTO images (image_id, iamge_name,  yaw, pitch, roll, height)  Values (

f = open("sql_query.txt", "a")
image_id = 0
for item in file:
    query1 = 'INSERT INTO images (image_id, image_name,  yaw, pitch, roll, height)  Values (' + str(image_id) + ',"' + item["image_name"] + '",' + str(item["yaw"]) + ',' + str(item['pitch']) + ',' + str(item['roll']) + ',' + str(item['height']) + ');'
    f.write(query1)
    for value in item["GPS"]:
        query2 = 'INSERT INTO gps (id, area, lat, lon) Values (' + str(image_id) + ',"' + str(value['area']) + '",' + str(value['lat']) + ',' + str(value['lon']) + ');'
        f.write(query2)
    
    for value in item["bombs"]:
        query3 ='INSERT INTO image_bombs (image_id, bomb_id, lat, lon) Values (' + str(image_id) + ',' + str(value['id']) + ',' + str(value['lat']) + ',' + str(value['lon']) + ');'
        f.write(query3)
    image_id += 1

f.close()