import json
import urllib.request
import cv2
import math
import matplotlib.path as mpltPath
import matplotlib.patches as patches
import pylab
import os
#########################################################################################################
# GPSCalc - takes provided image information and calculates the center GPS coordinate
#########################################################################################################
class GPSCalc:
#########################################################################################################
# init - initializes the GPSCalc class
# self.r_earth - radius of the earth
#########################################################################################################
	def __init__(self):
		self.r_earth = 6378
		
#########################################################################################################
# truncate - truncates a number to the specified number of decimals
# number - the number to truncate
# digits - the desired precision
#########################################################################################################		
	def truncate(self, number, digits) -> float:
		stepper = 10.0 ** digits 
		return math.trunc(stepper * number) / stepper

#########################################################################################################
# getElevation - finds the elevation of the supplied lat and long
# lat - the latitude of the image where you want to find the elevation
# lon - the longitude of the image where you want to find the elevation
#########################################################################################################
	def getElevation(self, lat, lon):
	  '''
	  uses a free api to get the evelation of the lat and long given
	  '''
	  url = "https://nationalmap.gov/epqs/pqs.php?x=" + str(lon) + "&y=" + str(lat) + "&units=Meters&output=json"
	  
	  response = urllib.request.urlopen(url)
	  data = json.loads(response.read())
	  temp = data["USGS_Elevation_Point_Query_Service"]
	  temp2 = temp['Elevation_Query']
	  elevation = temp2['Elevation']
	  return elevation

#########################################################################################################
# getGPS - finds the GPS coordinate of the center of an image
# img_w - the width of the image
# img_h - the height of the image
# elevation - the elevation of the area the image is located at, relative to sea level. found using getElevation
# lat - the image's latitude
# lon - the image's longitude
# alt - the altitude the camera was at when the image was taken
# filepath = the filepath to the image
#########################################################################################################
	def getGPS(self, img_w, img_h, elevation, lat, lon, alt, filepath):
		'''
		 this function does a lot of trig to get what gps cooridnate of each conor of the image
		 currently it is not as exact as needed. The issue could be do to no ground truth test flight
		 there is most likely a fudge factor that needs to be added in
		'''
		img = cv2.imread(filepath)
		print(img)
		yaw=0#, _, _= img.dls_pose() # change from true north, image we tested were always true north so 0 is hardcoded in 
		ar = img_h / img_w # aspect ratio
		# FOV = field of view
		FOV_hd = 48 #img.get_item('Composite:FOV') #horizontal degrees FOV, using micasense camera so just hardcoded in :( https://www.google.com/search?q=focal+length+micasense+altum&rlz=1C1CHBD_enUS849US849&oq=focal+length+micasense+altum&aqs=chrome..69i57.4248j0j7&sourceid=chrome&ie=UTF-8
		FOV_vd = FOV_hd * ar # img.get_item('Composite:FocalLength35elf') # vertical degrees FOV
		height = alt - elevation # above ground level value
		
		
		FOV_hr = math.radians(FOV_hd) # horizontal radians FOV
		FOV_vr = math.radians(FOV_vd) # vertical radians FOV
		
		#Bunch of math calculations, ask @LorchZachary
		d1 = height * math.tan(FOV_vr/2)
		d2 = height * math.tan(FOV_hr/2)
		d3  = math.sqrt(d1**2 + d2**2)
		lamda = math.atan(d1/d2) + (math.pi/2) - yaw
		x =  math.cos(lamda) * d3
		y = math.sin(lamda) * d3
		
		GPS = []
		#GPS.append((lat,lon))
		# corner one
		dx =x/1000
		dy = y/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = lon + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		# print("top right")
		#print(new_latitude, ",",new_longitude)
		GPS.append((self.truncate(new_latitude,7), self.truncate(new_longitude,7)))    

		# corner two
		dx =-y/1000
		dy = x/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = lon + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		# print("top left")
		#print(new_latitude, ",",new_longitude)
		GPS.append((self.truncate(new_latitude,7), self.truncate(new_longitude,7)))    
		
		# corner three
		dx =y/1000
		dy = -x/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = lon + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		#print("bottom right")
		#print(new_latitude, ",",new_longitude)
		GPS.append((self.truncate(new_latitude,7), self.truncate(new_longitude,7)))    
		
		# corner four
		dx =-x/1000
		dy = -y/1000
		new_latitude  = lat  + (dy / self.r_earth) * (180 / math.pi)
		new_longitude = lon + (dx / self.r_earth) * (180 / math.pi) /  math.cos(lat * math.pi/180)
		#print("bottom left")
		#print(new_latitude, ",",new_longitude)
		GPS.append((self.truncate(new_latitude,7), self.truncate(new_longitude,7)))
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
		

