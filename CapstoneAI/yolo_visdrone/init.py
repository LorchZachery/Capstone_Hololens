#########################################################################################################
# Author - C1C Jonathan Nash
# Last Updated - 17 Mar 2021
# Brief - holds the information that will be sent to the database
#########################################################################################################

#print("in init") #test stuff
#test = "howlong/will/this/filepath/go.jpg"

b_boxes = [] #bounding box information from the AI


#hardcoded image held in the test_images folder, taken from Google Earth and found GPS locations of all 4 corners, used for bounding box gps location calculation
name = "1.jpg"
#dictionary that holds all information in each relevant image provided to the AI
img_data = {}

#puts hardcoded image information into dictionary - all of this *can* be provided, but the only necessary information (assuming top-down image profile with no pitch/yaw and a sufficiently small area covered so that we can assume the area is flat, with the top facing north) is the gps coordinates of the four corners of the image (top_left, bottom_left, bottom_right, top_right) and the images height and width (img_h + img_w)
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