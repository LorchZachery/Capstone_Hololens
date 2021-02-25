import asyncio
import init

async def Catch(bbox):
	print("in async catch")
	info = bbox
	print("caught info: " + str(info))
	init.b_boxes.append(info)
	print("current b box array: " + str(init.b_boxes))
	successful = await json()
	if successful:
		print("successfully created json")
	return 1
	
async def json():
	img_data = {}
	#for img in init.b_boxes:
	#name = img[-1]
	name = "img1.png"
	img_data[name] = []
	img_data[name].append({
	'CAM' : 2312,
	'GROUND' : 2150,
	'top_left' : (39.011729, -104.885030),
	'bottom_left' : (39.011063, -104.995030),
	'bottom_right' : (39.011063, -104.883907),
	'top_right' : (39.011729, -104.885030)
	})
	#pixels
	img_h = 635
	img_w = 800
	
	cur_box = init.b_boxes[-1]
	print("cur box: " + str(cur_box))
	
	box_x, box_y, box_w, box_h = cur_box[0], cur_box[1], cur_box[2], cur_box[3]
	
	print("box info " + str(box_x) + ", "+ str(box_y) + ", "+ str(box_w) + ", "+ str(box_h))
	
	
