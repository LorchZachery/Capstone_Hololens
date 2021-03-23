# make sure you have piexif installed as well
# https://pypi.org/project/gpsphoto
from GPSPhoto import gpsphoto
import init
class ImageData:
	def __init__(self, file = None):
		filepath = file
		if filepath is None:
			img_loc = 'D:\HololensIED\CapstoneAI\\'
			img = 'loctets.jpeg'
			filepath = img_loc + img
	def getData(self):
		data = gpsphoto.getGPSData(filepath)
		rawData = gpsphoto.getRawData(filepath)
		init.img_data[img] = {}
		for tag in data.keys():
			print("%s: %s" % (tag, data[tag]))
			init.img_data[img][tag] = data[tag]
		#print("raw data")	
		#for tag in rawData.keys():
		#	print("%s: %s" % (tag, rawData[tag]))
		#print("temp")
		#print(init.temp)

		print("img data")
		print(init.img_data)