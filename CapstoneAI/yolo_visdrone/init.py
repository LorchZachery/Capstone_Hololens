#########################################################################################################
# Author - C1C Jonathan Nash
# Last Updated - 17 Mar 2021
# Brief - holds the information that will be sent to the database
#########################################################################################################

#print("in init") #test stuff
#test = "howlong/will/this/filepath/go.jpg"

from gps_coord import GPSCalc
from image_data import ImageData
import PIL
import os
import time
import asyncio

img_data = {}
b_boxes	 = []

class Init:
	def __init__(self, img_path=None):
		self.b_boxes = b_boxes #bounding box information from the AI
		self.img_data = img_data
		self.unaccess = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\Unaccessed_Images'
		self.access = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\Accessed_Images'
		self.access_path = True#False
		self.queue = []
		self.mutex = 1
		#if img_path is None:
		if len(os.listdir(self.unaccess)) == 0:
			#hardcoded image held in the test_images folder, taken from Google Earth and found GPS locations of all 4 corners, used for bounding box gps location calculation
			name = "1.jpg"
			#dictionary that holds all information in each relevant image provided to the AI
			print("init img path was none")
			#puts hardcoded image information into dictionary - all of this *can* be provided, but the only necessary information (assuming top-down image profile with no pitch/yaw and a sufficiently small area covered so that we can assume the area is flat, with the top facing north) is the gps coordinates of the four corners of the image (top_left, bottom_left, bottom_right, top_right) and the images height and width (img_h + img_w)
			self.img_data[name] = {
				'CAM' : 2312,
				'GROUND' : 2150,
				'top_left' : (39.011729, -104.885030), # img top left GPS coordinate (lat, lon)
				'bottom_left' : (39.011063, -104.885030), # img bottom left GPS coordinate
				'bottom_right' : (39.011063, -104.883907), # img bottom right GPS coordinate
				'top_right' : (39.011729, -104.883907), # img top right GPS coordinat
				'img_h' : 635,
				'img_w' : 800,
				}
				#39.0082142, -104.8858718
		else:
			self.access_path = True
			print("There are unaccessed images")
			'''data = ImageData(img_path)
			print(data)
			img_name = data.getData()
			gps_calc = GPSCalc()
			
			lat = self.img_data[img_name]['Latitude']
			lon = self.img_data[img_name]['Longitude']
			elevation = gps_calc.getElevation(lat, lon)
			altitude = self.img_data[img_name]['Altitude']
			print("elevation")
			print(str(elevation))
			
			img = PIL.Image.open(img_path)
			
			print(img)
			
			img_w, img_h = img.size
			
			print(img_w)
			print(img_h)
			gps = gps_calc.getGPS(img_w, img_h, elevation, lat, lon, altitude)
			
			print("gps")
			print(gps)
			
			self.img_data[img_name]['top_right'] = gps[0]
			self.img_data[img_name]['top_left'] = gps[1]
			self.img_data[img_name]['bottom_right'] = gps[2]
			self.img_data[img_name]['bottom_left'] = gps[3]'''
	
	async def look_for_image(self):
		if self.mutex == 2:
			print("waiting for mutex 1")
			return
		if len(os.listdir(self.unaccess)) == 0:		
			print("Unaccessed file empty")
		for img in os.listdir(self.unaccess):
			img_path = self.unaccess + "\\" + img
			if img not in img_data:
				
				self.mutex = 1
				
				print(img_path)
				data = ImageData(img_path)
				print(data)
				img_name = data.getData()
				gps_calc = GPSCalc()
				
				lat = self.img_data[img_name]['Latitude']
				lon = self.img_data[img_name]['Longitude']
				elevation = gps_calc.getElevation(lat, lon)
				altitude = self.img_data[img_name]['Altitude']
				print("elevation")
				print(str(elevation))
				
				img = PIL.Image.open(img_path)
				
				print(img)
				
				img_w, img_h = img.size
				
				img.close()
				print(img_w)
				print(img_h)
				gps = gps_calc.getGPS(img_w, img_h, elevation, lat, lon, altitude)
				
				print("gps")
				print(gps)
				
				self.img_data[img_name]['top_right'] = gps[0]
				self.img_data[img_name]['top_left'] = gps[1]
				self.img_data[img_name]['bottom_right'] = gps[2]
				self.img_data[img_name]['bottom_left'] = gps[3]
				print(img_name)
				img_new = self.access + '\\' + img_name
				
				print("moving " + img_name + " from unaccessed location to accessed location")
				os.rename(img_path, img_new)
				self.queue.append(img_new)
				self.mutex = 2
				
			else:
				os.remove(img_path)
		
	
	
	def get_img_data(self):
		print("returning img data:")
		print(self.img_data)
		return self.img_data