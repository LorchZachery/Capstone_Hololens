#######################################
# Author - Jonathan Nash
# Last Updated - 15 Mar 2021
# Brief - Asynchronous functions that will run while the AI object-detection function is running
#		  that will capture bounding box data and parse and format that data properly to be sent to
#  		  the database.
#######################################


import asyncio
import init


#######################################
# Catch - catch bounding box information for AI-detected "bombs" which are sent to this function; only runs when it 	  gets information 
# bbox - bounding box information sent from the AI, has the center width and height of the box
#######################################
async def Catch(bbox):
	#print("in async catch") #make sure we enter the function
	info = bbox 
	#print("caught info: " + str(info))
	init.b_boxes.append(info) # save the bounding box in the init script
	#print("current b box array: " + str(init.b_boxes))
	successful = await json() # send captured data to the dictionary (json)
	if successful: #make sure we actually did the above
		print("successfully created json")
	return 1 #return true to the function that called this one

#######################################
# json - parses captured bounding box data into a json format so that it can be sent to a database
#######################################	
async def json():
	#print("init img data 1") # make sure the function is entered
	#print(init.img_data) # prints out the current image data holder to check what is in it
	img_data = init.img_data # create local variable based off of main json data block
	#for img in init.b_boxes:
	#name = img[-1]
	
	#img_data[name] = []
	# append all necessary information, currently hardcoded for testing purposes. A new function will be needed
	# to extract all of this information from an image. The most important data is gps coordinates for the four 
	# corners.
	img_data[name].append({
	'CAM' : 2312,
	'GROUND' : 2150,
	'top_left' : (39.011729, -104.885030),
	'bottom_left' : (39.011063, -104.995030),
	'bottom_right' : (39.011063, -104.883907),
	'top_right' : (39.011729, -104.885030)
	})
	
	#pixels
	
	
	cur_box = init.b_boxes[-1]
	#print("cur box: " + str(cur_box))
	
	box_x, box_y = cur_box[0], cur_box[1]
	name = cur_box[2]
	
	#print("box info " + str(box_x) + ", "+ str(box_y))
	
	#find coords of center of each b box
	
	#print("top right lat: " + str(img_data[name]["top_right"][0]))
	
	
	gps_per_width = (abs(img_data[name]["top_left"][1] - img_data[name]["top_right"][1])) / (img_data[name]["img_w"] * 1.00000000)
	
	#print(gps_per_width)
	
	gps_per_height = (abs(img_data[name]["top_left"][0] - img_data[name]["bottom_left"][0])) / (img_data[name]["img_h"] * 1.00000000)
	
	#print(gps_per_height)
	
	gps_lon = gps_per_width * cur_box[0] + img_data[name]["top_left"][1]
	gps_lat = img_data[name]["top_left"][0] - gps_per_height * cur_box[1]
	
	gps_lon = '%.6f'%(gps_lon)
	gps_lat = '%.6f'%(gps_lat)
	
	img_data[name][(box_x, box_y)] = {}
	img_data[name][(box_x, box_y)]['lat'] = gps_lat
	img_data[name][(box_x, box_y)]['lon'] = gps_lon


	print("init img data 2")
	print(init.img_data)
	
	return 1