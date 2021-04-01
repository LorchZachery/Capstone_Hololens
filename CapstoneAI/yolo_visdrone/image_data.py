# make sure you have piexif installed as well
# https://pypi.org/project/gpsphoto
from GPSPhoto import gpsphoto
import init
class ImageData:
	def __init__(self, file = None):
		print("in init imagedata")
		print(file)
		self.filepath = file
		
		if self.filepath is None:
			self.img_loc = 'D:\HololensIED\CapstoneAI\\'
			self.img = 'loctets.jpeg'
			self.filepath = self.img_loc + self.img
		else:
			splits = self.filepath.split('\\')
			self.img = splits[-1]
			print("self.img")
			print(self.img)
			self.img_loc = self.filepath[:-len(self.img)]
			print("img loc")
			print(self.img_loc)
	def getData(self):
		data = gpsphoto.getGPSData(self.filepath)
		rawData = gpsphoto.getRawData(self.filepath)
		init.img_data[self.img] = {}
		for tag in data.keys():
			print("%s: %s" % (tag, data[tag]))
			init.img_data[self.img][tag] = data[tag]
		#print("raw data")	
		#for tag in rawData.keys():
		#	print("%s: %s" % (tag, rawData[tag]))
		#print("temp")
		#print(init.temp)

		print("img data")
		print(init.img_data)
		return self.img