#########################################################################################################
# Author - C1C Jonathan Nash, @JonathanNash21
# Last Updated - 17 Mar 2021
# Brief - Asynchronous functions that will run while the AI object-detection function is running
#		  that will capture bounding box data and parse and format that data properly to be sent to
#  		  the database.
#########################################################################################################


import asyncio
import init
from gps_coord import GPSCalc 


#########################################################################################################
# Catch - catch bounding box information for AI-detected "bombs" which are sent to this function; only runs when it 	  gets information 
# bbox - bounding box information sent from the AI, has the center width and height of the box
#########################################################################################################
async def Catch(bbox, ):
	#print("in async catch") #make sure we enter the function
	info = bbox 
	#print("caught info: " + str(info))
	init.b_boxes.append(info) # save the bounding box in the init script
	#print("current b box array: " + str(init.b_boxes))
	successful = await json() # send captured data to the dictionary (json)
	if successful: #make sure we actually did the above
		print("successfully created json")
	return 1 #return true to the function that called this one

#########################################################################################################
# json - parses captured bounding box data into a json format so that it can be sent to a database
#########################################################################################################	
async def json():
	print("init img data 1") # make sure the function is entered
	print(init.img_data) # prints out the current image data holder to check what is in it
	img_data = init.img_data # create local variable based off of main json data block
	#for img in init.b_boxes:
	#name = img[-1]
	
	#img_data[name] = []
	# append all necessary information, currently hardcoded for testing purposes. A new function will be needed
	# to extract all of this information from an image. The most important data is gps coordinates for the four 
	# corners of the image. 
	'''We might have code elsewhere that will find the 4 coordinates based off a center-focused GPS coordinate'''
	# DO NOT USE THIS ONE, DICTIONARY INITIALIZED IN init.py
	"""img_data[name].append({
	'CAM' : 2312, # camera height
	'GROUND' : 2150, # ground height
	'top_left' : (39.011729, -104.885030), # img top left GPS coordinate (lat, lon)
	'bottom_left' : (39.011063, -104.885030), # img bottom left GPS coordinate
	'bottom_right' : (39.011063, -104.883907), # img bottom right GPS coordinate
	'top_right' : (39.011729, -104.883907) # img top right GPS coordinate
	})"""
		
	cur_box = init.b_boxes[-1] # grab the most recent bounding box found by the AI
	#print("cur box: " + str(cur_box))
	
	box_x, box_y = cur_box[0], cur_box[1] # grab the bounding box's center x and y coordinate
	name = cur_box[2] # grab the img name
	
	#print("box info " + str(box_x) + ", "+ str(box_y))
		
	# find the change in GPS value per coordinate across the x axis (longitude change)
	#print(img_data[name])
	#if type(img_data[name]) != tuple:
	#	return 0
	gps_per_width = (abs(img_data[name]["top_left"][1] - img_data[name]["top_right"][1])) / (img_data[name]["img_w"] * 1.00000000)
	
	#print(gps_per_width)
	
	# find the change in GPS value per coordinate across the y axis (latitude change)
	gps_per_height = (abs(img_data[name]["top_left"][0] - img_data[name]["bottom_left"][0])) / (img_data[name]["img_h"] * 1.00000000)
	
	#print(gps_per_height)
	
	# calculate the bounding box's lon and lat
	gps_lon = gps_per_width * cur_box[0] + img_data[name]["top_left"][1] # multiply the lon change per pixel with the x coordinate of the bounding box and then add the top left x coordinate to that value
	gps_lat = img_data[name]["top_left"][0] - gps_per_height * cur_box[1] # multiply the lat change per pixel with the y coordinate of the bounding box and then subtract that from the top left y coordinate
	
	# limit the lat and lon values to 6 decimals
	gps_lon = '%.6f'%(gps_lon) 
	gps_lat = '%.6f'%(gps_lat)
	
	# create a dictionary for this box's coordinate value inside the current image we are working with
	img_data[name][(box_x, box_y)] = {}
	
	#assign lat value to this dictionary entry
	img_data[name][(box_x, box_y)]['lat'] = gps_lat
	#assign lon value to this dictionary entry
	img_data[name][(box_x, box_y)]['lon'] = gps_lon


	print("init img data 2")
	print(init.img_data)
		
	#return successful completion of the funtion
	return 1
