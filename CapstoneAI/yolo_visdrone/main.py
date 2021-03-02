from obj_det_custom_yolo_live import Adjusted
import os
import init
from asynchronous import Catch
import asyncio
from dp_connect import insert_latlon as update

#print(init.x)


imgset = 'D:\HololensIED\CapstoneAI\yolo_visdrone\\test_images'

# print(os.listdir(imgset))
adj = Adjusted()
"""
for img in os.listdir(imgset):
    img = imgset + "\\" + img
    # print(img)
    
    adj.testRun(img)
"""
#asyncio.run(Catch)
adj.testRun()
for img in init.img_data:
	for box in img:
		if type(box) is not dict:
			continue
		update(box['lat'], box['lon'])