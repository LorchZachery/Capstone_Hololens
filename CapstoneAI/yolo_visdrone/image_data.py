# make sure you have piexif installed as well
# https://pypi.org/project/gpsphoto
from GPSPhoto import gpsphoto
import init
img_loc = 'D:\HololensIED\CapstoneAI\\'
img = 'loctets.jpeg'

data = gpsphoto.getGPSData(img_loc+img)
rawData = gpsphoto.getRawData(img_loc+img)
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