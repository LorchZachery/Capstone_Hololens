print("in init")
semaphore = 0
test = "howlong/will/this/filepath/go.jpg"
b_boxes = []
x = 2


pic_name = test.split("/")

pic_name = pic_name[-1]


print(pic_name)

name = "1.jpg"
img_data = {}
img_data[name] = {
	'CAM' : 2312,
	'GROUND' : 2150,
	'top_left' : (39.011729, -104.885030),
	'bottom_left' : (39.011063, -104.885030),
	'bottom_right' : (39.011063, -104.883907),
	'top_right' : (39.011729, -104.883907),
	'img_h' : 635,
	'img_w' : 800
	}