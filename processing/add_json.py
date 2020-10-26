import json
import urllib.request
import micasense.metadata as metadata
import math
import matplotlib.path as mpltPath
import matplotlib.patches as patches
import pylab
import os

r_earth = 6378
directory = '../test_data/'
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def getElevation(lat, long):
  '''
  uses a free api to get the evelation of the lat and long given
  '''
  url = "https://nationalmap.gov/epqs/pqs.php?x=" + long + "&y=" + lat + "&units=Meters&output=json"
  
  response = urllib.request.urlopen(url)
  data = json.loads(response.read())
  temp = data["USGS_Elevation_Point_Query_Service"]
  temp2 = temp['Elevation_Query']
  elevation = temp2['Elevation']
  return elevation


def getGPS(img, elevation, lat, long, alt):
    '''
     this function does a lot of trig to get what gps cooridnate of each conor of the image
     currently it is not as exact as needed. The issue could be do to no ground truth test flight
     there is most likely a fudge factor that needs to be added in
    '''
    yaw, _, _= img.dls_pose()
    im_w, im_h = img.image_size() 
    ar = im_h / im_w
    FOV_hd = img.get_item('Composite:FOV')
    FOV_vd = FOV_hd * ar # img.get_item('Composite:FocalLength35elf')
    height = alt - elevation
    
    
    FOV_hr = math.radians(FOV_hd)
    FOV_vr = math.radians(FOV_vd)
    d1 = height * math.tan(FOV_vr/2)
    d2 = height * math. tan(FOV_hr/2)
    d3  = math.sqrt(d1**2 + d2**2)
    lamda = math.atan(d1/d2) + (math.pi/2) - yaw
    x =  math.cos(lamda) * d3
    y = math.sin(lamda) * d3
    
    GPS = []
    #GPS.append((lat,long))
    # corner one
    dx =x/1000
    dy = y/1000
    new_latitude  = lat  + (dy / r_earth) * (180 / math.pi)
    new_longitude = long + (dx / r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
    # print("top right")
    #print(new_latitude, ",",new_longitude)
    GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    

    # corner two
    dx =-y/1000
    dy = x/1000
    new_latitude  = lat  + (dy / r_earth) * (180 / math.pi)
    new_longitude = long + (dx / r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
    # print("top lelft")
    #print(new_latitude, ",",new_longitude)
    GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    
    
    # corner three
    dx =y/1000
    dy = -x/1000
    new_latitude  = lat  + (dy / r_earth) * (180 / math.pi)
    new_longitude = long + (dx / r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
    #print("bottom right")
    #print(new_latitude, ",",new_longitude)
    GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    
    
    # corner four
    dx =-x/1000
    dy = -y/1000
    new_latitude  = lat  + (dy / r_earth) * (180 / math.pi)
    new_longitude = long + (dx / r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
    #print("bottom left")
    #print(new_latitude, ",",new_longitude)
    GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))
    return GPS



def checkingIfBomb(GPS, bombCoors):
    # converting to polar coord=indates to order correctly to check if bomb is inside
    cent=(sum([p[0] for p in GPS])/len(GPS),sum([p[1] for p in GPS])/len(GPS))
    GPS.sort(key=lambda p: math.atan2(p[1]-cent[1],p[0]-cent[0]))
    
    
    path = mpltPath.Path(GPS)
    
    locations = []
    # checking if the bomb is in the image
    for bomb in bombCoors:
        inside = path.contains_points([(bomb[0],bomb[1])])
        if inside[0]:
            locations.append((bomb))
    return GPS, locations
    
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data,f,indent =4)

def createJson(filename, bombCoors):
    filepath = directory + filename
    img = metadata.Metadata(filepath)
    lat = img.get_item('Composite:GPSLatitude')
    long = img.get_item('Composite:GPSLongitude')
    yaw, pitch, roll = img.dls_pose()
    alt = img.get_item('Composite:GPSAltitude')
    elevation = getElevation(str(lat),str(long))
    GPS, bombs = checkingIfBomb(getGPS(img, elevation, lat, long, alt), bombCoors)
    image_name = filename.split('.')[0][:-2] + '_stacked.tiff'
    data = {
        "image_name" : image_name,
        "yaw" : yaw,
        "pitch" : pitch,
        "roll": roll,
        "height" : alt - elevation, 
        "GPS" : [
            {"area" : "center", "lat" : lat, "long": long},
            {"area": "top right", "lat" :GPS[0][0], "long": GPS[0][1]},
            {"area": "top left", "lat" :GPS[1][0], "long": GPS[1][1]},
            {"area": "bottom right", "lat" :GPS[2][0], "long": GPS[2][1]},
            {"area": "bottom left", "lat" :GPS[3][0], "long": GPS[3][1]}
        ],
        "bombs" : [
        ],
    }
    for index, bomb in enumerate(bombs):
        item = {"id" : index , "lat" : bomb[0], "long" : bomb[1]}
        data["bombs"].append(item)
    
    print(json.dumps(data, indent=4, sort_keys=True))
    print()
    meta_json = os.path.join('stacked', 'metadata.json')
    with open(meta_json) as json_file:
        curr_data = json.load(json_file)
        
        temp= curr_data["images"]
        if( len(temp) == 0):
            temp.append(data)
        else:
            append = True
            for image in temp:
                if(image["image_name"] == data["image_name"]):
                    append = False
            if append:
                temp.append(data)
  
    write_json(curr_data, meta_json)
    
    
    
    
    