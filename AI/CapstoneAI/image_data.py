# make sure you have piexif installed as well
# https://pypi.org/project/gpsphoto
from GPSPhoto import gpsphoto
import init

#########################################################################################################
# ImageData - parses out meta data from images to be used for GPS calculations
#########################################################################################################
class ImageData:
#########################################################################################################
# init - initialize the ImageData class
# self.filepath - file path to the image we want to parses
# self.img - the image's name
# self.img_loc - the file path to the image's location
# 
#########################################################################################################
	def __init__(self, file = None):
		#print("in init imagedata")
		#print(file)
		self.filepath = file
		# default filepath for testing purposes
		if self.filepath is None:
			self.img_loc = 'D:\HololensIED\CapstoneAI\yolo_visdrone\geolocation_imgs\\'
			self.img = 'loctets.jpeg'
			self.filepath = self.img_loc + self.img
		else:
			#split the supplied filepath based on \\ so we can extract the image name
			splits = self.filepath.split('\\')
			self.img = splits[-1] # get the image name
			#print("self.img")
			#print(self.img)
			self.img_loc = self.filepath[:-len(self.img)] #get the file path
			#print("img loc")
			#print(self.img_loc)
	
#########################################################################################################
# getData - parses out the image's metadata
# data - holds all of the GPS data from the supplied image
# rawData - holds all of the raw data from the supplied image
#########################################################################################################
	def getData(self):
		data = gpsphoto.getGPSData(self.filepath)
		rawData = gpsphoto.getRawData(self.filepath)
		init.img_data[self.img] = {} # create a new entry in the main dictionary with the image name as the key, and its value a new dictionary
		for tag in data.keys(): # for each of the extracted data pieces (lat, lon, alt)
			#print("%s: %s" % (tag, data[tag]))
			init.img_data[self.img][tag] = data[tag] # supply the tag information to the dictionary
		#print("raw data")	
		#for tag in rawData.keys(): # not necessary
			#print("%s: %s" % (tag, rawData[tag]))
	

		#print("img data") # for showing that the dictionary actually updated
		#print(init.img_data)
		return self.img #return the image name