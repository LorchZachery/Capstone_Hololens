# yolo_visdrone

yolov4-tiny retrained on visdrone2019 aerial data.

best run thru opencv with

    	net = cv2.dnn.readNetFromDarknet(in_config, in_weights)
    	net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    	net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    	layers = net.getLayerNames()
    	output_layers = [layers[i[0] - 1] for i in net.getUnconnectedOutLayers()]

inference with
	
	blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), swapRB=True, crop=False)
    	net.setInput(blob)
    	layer_outputs = net.forward(output_layers)


