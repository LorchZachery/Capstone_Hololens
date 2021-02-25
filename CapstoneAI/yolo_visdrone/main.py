from obj_det_custom_yolo_live import Adjusted
import os
import init
from asynchronous import Catch
import asyncio

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