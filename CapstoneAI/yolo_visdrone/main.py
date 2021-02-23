from obj_det_custom_yolo_live import Adjusted
import os
import init

print(init.x)


imgset = 'F:\CapstoneAI Images\cars_train'

# print(os.listdir(imgset))
adj = Adjusted()
"""
for img in os.listdir(imgset):
    img = imgset + "\\" + img
    # print(img)
    
    adj.testRun(img)
"""
adj.testRun()