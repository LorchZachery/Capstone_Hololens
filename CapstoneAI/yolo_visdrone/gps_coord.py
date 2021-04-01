import json
import urllib.request

import math
import matplotlib.path as mpltPath
import matplotlib.patches as patches
import pylab
import os

class GPSCalc:
	
	def __init__(self):
		self.r_earth = 6378
		self.directory = '../data/'
		
		
	def truncate(number, digits) -> float:
		stepper = 10.0 ** digits
		return math.trunc(stepper * number) / stepper

	def getElevation(self, lat, long):
	  '''
	  uses a free api to get the evelation of the lat and long given
	  '''
	  url = "https://nationalmap.gov/epqs/pqs.php?x=" + str(long) + "&y=" + str(lat) + "&units=Meters&output=json"
	  
	  response = urllib.request.urlopen(url)
	  data = json.loads(response.read())
	  temp = data["USGS_Elevation_Point_Query_Service"]
	  temp2 = temp['Elevation_Query']
	  elevation = temp2['Elevation']
	  return elevation


	def getGPS(self, img, elevation, lat, long, alt1):
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
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = long + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		# print("top right")
		#print(new_latitude, ",",new_longitude)
		GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    

		# corner two
		dx =-y/1000
		dy = x/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = long + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		# print("top lelft")
		#print(new_latitude, ",",new_longitude)
		GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    
		
		# corner three
		dx =y/1000
		dy = -x/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = long + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		#print("bottom right")
		#print(new_latitude, ",",new_longitude)
		GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))    
		
		# corner four
		dx =-x/1000
		dy = -y/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = long + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		#print("bottom left")
		#print(new_latitude, ",",new_longitude)
		GPS.append((truncate(new_latitude,7), truncate(new_longitude,7)))
		return GPS



	def checkingIfBomb(self, GPS, bombCoors):
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
		

