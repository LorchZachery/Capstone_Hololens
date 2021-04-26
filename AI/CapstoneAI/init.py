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

#the main dictionary that holds all important information for the database - image name, corner coordinates, altitude, elevation, AI-detected bomb locations
img_data = {}
#an array of bounding boxes for asynchronous.py
b_boxes	 = []


#########################################################################################################
# Init - Class that holds all important information for the database
#########################################################################################################

class Init:
#########################################################################################################
# init - initialize the Init class
# self.b_boxes - self access for b_boxes so the global is not updated by this class if a second Init() is run
# self.img_data - self access for img_data so the global is not updated by this class if a second Init() is run
# self.unaccess - file path to the unaccessed images - any images you want to put in the dictionary/run through the AI should be put in here
# self.access - file path to the accessed images - no images should be placed in here if you want to parse them, the code will place accessed images here so they do not stay in unaccessed
# self.access_path - for testing only, allows for the hardcoded data to be used in the below if-statement, was only for proof of concept and probably isn't necessary anymore
# self.queue - an array of images, put in place in case look_for_image runs multiple times before the AI, guaranting the AI will run through every image. Also facilitates supplying the file path to the 
# 			   AI
# self.mutex - mutual exclusion variable to (hopefully) prevent the AI from running on the accessed folder while look_for_image is moving a new image to the accessed folder, and vice versa
#########################################################################################################
	def __init__(self):
		self.b_boxes = b_boxes #bounding box information from the AI
		self.img_data = img_data
		self.unaccess = 'D:\HololensIED\CapstoneAI\\Unaccessed_Images'
		self.access = 'D:\HololensIED\CapstoneAI\\Accessed_Images'
		self.access_path = True#False #make false when you want to run the spoofed image
		self.queue = []
		self.mutex = 1
		
		# testing purposes only, allows to show an image with vehicles the AI will detect with "coordinates" - image is a screenshot from Google earth and we plotted the 4 corners using Google Earth's coordinate system. This is still useful because we do not have any images with embedded coordinate data that contain cars (Only using HALO Group images, which have coordinate information but literally nothing else of worth)
		if not self.access_path:
			#hardcoded image held in the test_images folder, taken from Google Earth and found GPS locations of all 4 corners, used for bounding box gps location calculation
			name = "1.jpg"
			
			print("TESTING ONLY - using car image with spoofed GPS coordinates")
			#puts hardcoded image information into dictionary - all of this *can* be provided, but the only necessary information (assuming top-down image profile with no pitch/yaw and a sufficiently small area covered so that we can assume the area is flat, with the top facing north) is the gps coordinates of the four corners of the image (top_left, bottom_left, bottom_right, top_right) and the images height and width (img_h + img_w)
			self.img_data[name] = {
				'Altitude' : 2312,
				'Elevation' : 2150,
				'top_left' : (39.011729, -104.885030), # img top left GPS coordinate (lat, lon)
				'bottom_left' : (39.011063, -104.885030), # img bottom left GPS coordinate
				'bottom_right' : (39.011063, -104.883907), # img bottom right GPS coordinate
				'top_right' : (39.011729, -104.883907), # img top right GPS coordinate
				'img_h' : 635,
				'img_w' : 800,
				}
			self.queue.append("D:\HololensIED\CapstoneAI\test_images\\1.jpg")
				#39.0082142, -104.8858718
		#  else:
			#self.access_path = True #used in main.py
			#print("There are unaccessed images")

#########################################################################################################
# look_for_image - looks through the unaccessed directory and takes any images in there and parses out the necessary information for calculating the GPS coordinates of each detected bomb. If an image has already been accessed an is re-added to the unaccessed directory, the image will be tossed out (this requires the program to have been running when the image was initially parsed, otherwise you will get an os error)
#########################################################################################################
	async def look_for_image(self):
		# prevent running the function if the AI is running on an image(s) in the accessed directory
		if self.mutex == 2:
			print("waiting for mutex 1")
			return
		# print if the unaccessed directory is empty
		if len(os.listdir(self.unaccess)) == 0:		
			print("Unaccessed file empty")
		# run through each image (should be asynchronous, can also make it run through one at a time and have the AI run after each image if this becomes an issue)
		for img in os.listdir(self.unaccess):
			img_path = self.unaccess + "\\" + img #append the image name to the unaccessed file path
			if img not in img_data: # make sure we haven't already parsed this image
				
				self.mutex = 1 # lock the mutex
				
				#print(img_path)
				data = ImageData(img_path) #get the image's information ->image_data.py
				#print(data)
				img_name = data.getData()
				gps_calc = GPSCalc() # instantiate the GPSCalc class -> gps_coord.py
				
				lat = self.img_data[img_name]['Latitude'] # latitude that was extracted in image_data.py
				lon = self.img_data[img_name]['Longitude']# longitude that was extracted in image_data.py
				elevation = gps_calc.getElevation(lat, lon) # get the elevation -> gps_coord.py
				altitude = self.img_data[img_name]['Altitude'] # # altitude that was extracted in image_data.py
				#print("elevation")
				#print(str(elevation))
				
				img = PIL.Image.open(img_path) # open the image in pillow to dynamically get the dimensions
				
				#print(img)
				
				img_w, img_h = img.size # image dimensions
				
				img.close() # close the image - not doing this will cause issues when trying to move the image from one folder to the other later on
				#print(img_w)
				#print(img_h)
				gps = gps_calc.getGPS(img_w, img_h, elevation, lat, lon, altitude, img_path) # get the GPS value for the center of the image -> gps_coord.py
				
				#print("gps")
				#print(gps)
				
				#append the dictionary with the corner gps coordinates
				self.img_data[img_name]['top_right'] = gps[0]
				self.img_data[img_name]['top_left'] = gps[1]
				self.img_data[img_name]['bottom_right'] = gps[2]
				self.img_data[img_name]['bottom_left'] = gps[3]
				#print(img_name)
				img_new = self.access + '\\' + img_name # new file path for the image since it has been accessed now
				try:
					print("moving " + img_name + " from unaccessed location to accessed location")
					os.rename(img_path, img_new) # move this image to the accessed folder
					self.queue.append(img_new) # put the image in queue to be accessed by the AI
					self.mutex = 2
				except FileExistsError:
					print("Error, file " + img_name + " already exists in accessed folder, deleting file instead.")
					os.remove(img_path)
					pass
				
			else: # if the image placed in the unaccessed folder has already been parsed, remove it
				print(img + " has already been accessed. Deleting from unaccessed directory.")
				os.remove(img_path)
		
	
	
	def get_img_data(self):
		print("returning img data:")
		print(self.img_data)
		return self.img_data
