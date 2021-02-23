import asyncio
import init

async def Catch(bbox):
	print("in async catch")
	info = bbox
	print("caught info: " + str(info))
	init.b_boxes.append(info)
	print("current b box array: " + str(init.b_boxes))
	return 1
	