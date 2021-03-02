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
	'top_left' : (39.0082142, -104.8858718),
	'bottom_left' : (39.0081569, -104.8858718),
	'bottom_right' : (39.0081569, -104.8858002),
	'top_right' : (39.0082142, -104.8858002),
	'img_h' : 635,
	'img_w' : 800
	}
	#39.0082142, -104.8858718