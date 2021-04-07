#########################################################################################################
# Author - Dr. Steven Novotny, @stevenjnovotny
# Contributer - C1C Jonathan Nash, @JonathanNash21
# Last Updated - 17 Mar 2021
# Brief - Takes in an image(s) or video stream and passes that information to an AI which will look for
# 		  vehicles and encloses found vehicles in a unique bounding box. This information is then passed
#   	  on to asynchronous.py, which will handle GPS calculations and data formatting to submit to the 
#		  database.
#########################################################################################################

import cv2
import numpy as np
import asyncio
from asynchronous import Catch
import init


"""
use custom yolo to evaluate video stream
"""


class Adjusted:
#########################################################################################################
# init - initializethe Adjusted class
# self.CONF_THRESH - confidence threshold for whether an AI will display a bounding box or not
# self.NMS_THRESH - non maximum suppression threshold, helps prevent bounding boxes from overlapping
# self.output_layers - 
# self.frame_h - height of the image
# self.frame_w - width of the image
# self.myColor - used for text writing
# self.names - name of the image
#########################################################################################################
	def __init__(self):
		self.CONF_THRESH, self.NMS_THRESH = 0.01, 0.5
		self.output_layers, self.frame_h, self.frame_w, self.myColor = [], None, None, None
		self.names = []
		self.data_struct = init.img_data
		
#########################################################################################################
# detect_annotate - runs the image through the AI and annotates all discovered vehicles in bounding boxes
#                   and also sends the bounding box information to UpdateBBox
# self - self value for class
# img - the image that the AI will look at
# net - neural net weights and configuration
# classes - different classifications the AI will look for
#########################################################################################################
	def detect_annotate(self, img, net, classes):

		blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
		net.setInput(blob)
		layer_outputs = net.forward(self.output_layers)

		class_ids,confidences, b_boxes = [], [], []
		# print(layer_outputs)
		#btext = open("boundingBoxes.txt", "w")
		for output in layer_outputs:

			for detection in output:
				scores = detection[5:]
				class_id = np.argmax(scores)
				confidence = scores[class_id]
				# print('{:.6E}'.format(confidence))
				if confidence > self.CONF_THRESH:
					# print(detection)
					# print('{:.2E}'.format(confidence))
					center_x, center_y, w, h = (detection[0:4] * np.array(
						[self.frame_w, self.frame_h, self.frame_w, self.frame_h])).astype('int')

					x = int(center_x - w / 2)
					y = int(center_y - h / 2)

					#self.info["center"] = (center_x, center_y)


					b_boxes.append([x, y, int(w), int(h)])
					
					# information that will be sent to asynchronous.py, bounding box's center x and y coordinate (on the image, not GPS) and the image name
					B_Box = [center_x, center_y] + [self.names[-1]]
					B_Box.append(self.names[-1])
					
					# update the main dictionary (held in init.py) asynchronously
					asyncio.run(UpdateBBox(B_Box))
					#bbox = "x: " + str(b_boxes[-1][0]) + ", y: " + str(b_boxes[-1][1]) + ", w: " + str(b_boxes[-1][2]) + ", h: " + str(b_boxes[-1][3]) + "\n"
				   # btext.write(bbox)
					confidences.append(float(confidence))
					class_ids.append(int(class_id))
					print(class_id)
					print(classes[class_id])
					init.img_data[self.names[-1]][(center_x, center_y)]["classification"] = classes[class_id]
		#btext.close()
		if len(b_boxes) > 0:
			# Perform non maximum suppression for the bounding boxes to filter overlapping and low confidence bounding boxes
			indices = cv2.dnn.NMSBoxes(b_boxes, confidences, self.CONF_THRESH, self.NMS_THRESH).flatten()
			# print('classes: {}   indices: {}'.format(len(classes), len(indices)))
			# if len(indices) > 0:
			#     indices = indices.flatten()
			for index in indices:
				#print(index)
				print(b_boxes[index])
				#print(class_ids[index])
				x, y, w, h = b_boxes[index]
				cv2.rectangle(img, (x, y), (x + w, y + h), (20, 20, 230), 2)
				cv2.putText(img, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, self.myColor, 2)
				print(classes[class_ids[index]])
				#init.img_data[self.names[-1]][(X, Y)]["classification"] = classes[class_ids[index]] 
		else:
			cv2.putText(img, "Nothing found", (10, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, (0, 0,255), 2)

#########################################################################################################
# AIRun - sets up all the necessary information for the AI to be able to parse through an image
# self - self reference for class structure
# filename - allows a specific image to be passed in when the function is called, allows for multiple images
# 			 to be sent at a time.
#########################################################################################################
	def AIRun(self, filename=None):
	# if __name__ == '__main__':

		video_stream = False
		image_file = "test_images/1.jpg"
		if filename!=None:
			image_file = filename
		in_weights = 'yolov4-tiny-custom_last.weights'
		in_config = 'yolov4-tiny-custom.cfg'
		name_file = 'custom.names'

		#self.names.append(image_file.split("/")[-1])
		self.names.append(image_file.split("\\")[-1].split("/")[-1])
		print(self.names[-1])
		#cv2.waitKey(0)

		# load names
		with open(name_file, "r") as f:
			classes = [line.strip() for line in f.readlines()]
		print(classes)

		# Load the network
		net = cv2.dnn.readNetFromDarknet(in_config, in_weights)
		net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
		layers = net.getLayerNames()
		self.output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

		if video_stream:
			# cap = cv2.VideoCapture(0)
			cap = cv2.VideoCapture('test_video.mov')
			# s

			success, img = cap.read()
			self.frame_h, self.frame_w = img.shape[:2]

			print('image: {} x {} pixels'.format(self.frame_w, self.frame_h))

			blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
			net.setInput(blob)
			layer_outputs = net.forward(self.output_layers)

			colors = np.random.uniform(0, 255, size=(len(classes), 3))
			myColor = (20, 20, 230)

			while True:
				timer = cv2.getTickCount()
				success, img = cap.read()

				if not success:
					break

				self.detect_annotate(img, net, classes)

				fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

				myColor = (20, 20, 230)
				cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2)
				cv2.imshow("Tracking", img)
				if cv2.waitKey(1) & 0xff == ord('q'):
					break
		else:
			img = cv2.imread(image_file)
			height, width = img.shape[:2]
			self.frame_h, self.frame_w = img.shape[:2]

			print('image: {} x {} pixels'.format(self.frame_w, self.frame_h))

			blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
			net.setInput(blob)
			layer_outputs = net.forward(self.output_layers)
			# print(layer_outputs)

			colors = np.random.uniform(0, 255, size=(len(classes), 3))
			myColor = (20, 20, 230)

			self.detect_annotate(img, net, classes)

			cv2.imshow("Result", img)
			cv2.waitKey(0)
			
#########################################################################################################
# UpdateBBox - updates the initial dictionary with the newest bounding box information
# B_Box - the newest bounding box information to be added to the dictionary
#########################################################################################################
async def UpdateBBox(B_Box):
	#print("in update BBox")
	#print("BBox received: " + str(B_Box))
	successful = await Catch(B_Box)
	if successful:
		print("everything works")
	
		
		