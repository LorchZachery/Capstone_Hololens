import cv2
import numpy as np
import asyncio
from asynchronous import Catch


"""
use custom yolo to evaluate video stream
"""


class Adjusted:
	def __init__(self):
		self.CONF_THRESH, self.NMS_THRESH = 0.01, 0.5
		self.output_layers, self.frame_h, self.frame_w, self.myColor = [], None, None, None
		self.names = []

	def detect_annotate(self, img, net, classes):

		blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
		net.setInput(blob)
		layer_outputs = net.forward(self.output_layers)

		class_ids, confidences, b_boxes = [], [], []
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
					B_Box = b_boxes[-1] + [self.names[-1]]
					#B_Box.append(self.names[-1])
					
					asyncio.run(UpdateBBox(B_Box))
					#bbox = "x: " + str(b_boxes[-1][0]) + ", y: " + str(b_boxes[-1][1]) + ", w: " + str(b_boxes[-1][2]) + ", h: " + str(b_boxes[-1][3]) + "\n"
				   # btext.write(bbox)
					confidences.append(float(confidence))
					class_ids.append(int(class_id))

		#btext.close()
		if len(b_boxes) > 0:
			# Perform non maximum suppression for the bounding boxes to filter overlapping and low confidence bounding boxes
			indices = cv2.dnn.NMSBoxes(b_boxes, confidences, self.CONF_THRESH, self.NMS_THRESH).flatten()
			# print('classes: {}   indices: {}'.format(len(classes), len(indices)))
			# if len(indices) > 0:
			#     indices = indices.flatten()
			for index in indices:
				#print(b_boxes[index])
				x, y, w, h = b_boxes[index]
				cv2.rectangle(img, (x, y), (x + w, y + h), (20, 20, 230), 2)
				cv2.putText(img, classes[class_ids[index]], (x + 5, y + 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, self.myColor,
							2)

	def testRun(self, filename=None):
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
			
	
async def UpdateBBox(B_Box):
	#print("in update BBox")
	print("BBox received: " + str(B_Box))
	successful = await Catch(B_Box)
	if successful:
		print("everything works")
	
		
		