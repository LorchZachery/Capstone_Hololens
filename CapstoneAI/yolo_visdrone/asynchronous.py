import asyncio
import init

async def Catch(bbox):
	#print("in async catch")
	info = bbox
	#print("caught info: " + str(info))
	init.b_boxes.append(info)
	#print("current b box array: " + str(init.b_boxes))
	successful = await json()
	if successful:
		print("successfully created json")
	return 1
	
async def json():
	print("init img data 1")
	print(init.img_data)
	img_data = init.img_data
	#for img in init.b_boxes:
	#name = img[-1]
	
	#img_data[name] = []
	"""img_data[name].append({
	'CAM' : 2312,
	'GROUND' : 2150,
	'top_left' : (39.011729, -104.885030),
	'bottom_left' : (39.011063, -104.995030),
	'bottom_right' : (39.011063, -104.883907),
	'top_right' : (39.011729, -104.885030)
	})"""
	
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
	
	img_data[name][(box_x, box_y)] = {}
	img_data[name][(box_x, box_y)]['lat'] = gps_lat
	img_data[name][(box_x, box_y)]['lon'] = gps_lon


	print("init img data 2")
	print(init.img_data)
	
	return 1