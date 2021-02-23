import cv2
import numpy as np
import random as rng

# Read image from webcam
frame_w = 640
frame_h = 480

cap = cv2.VideoCapture(0)
cap.set(3, frame_w)
cap.set(4, frame_h)

success, img = cap.read()
# frame_w = img.shape[1]
# frame_h = img.shape[0]
print('image size {} x {}'.format(frame_w, frame_h))

position = ()
tracking = False
def onMouse(event, x, y, flags, param):
    global position, tracking
    if event == cv2.EVENT_LBUTTONDOWN:
       print('x = %d, y = %d'%(x, y))
       position = (x,y)
       tracking = False
       print('finding ROI: ', not tracking)

cv2.namedWindow('image')
cv2.setMouseCallback('image', onMouse)

cv2.imshow('image',img)

# detector = cv2.SimpleBlobDetector_create()

#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
tracker = cv2.TrackerCSRT_create()  # ensures enlarging and localization of the selected region and improved tracking of the non-rectangular regions or objects. It uses only 2 standard features (HoGs and Colornames)
#tracker = cv2.TrackerMOSSE_create()  #  good accuracy; loses with quick movements
tracker.save('tracker_params.json')

#fs = cv2.FileStorage("tracker_params.json", cv2.FileStorage_READ)
#tracker.read(fs.getFirstTopLevelNode())

display_boxes = []
display_scores = []
counter = 0
display_box = None

while True:

    success, img = cap.read()
    #print('{} tracking: {}'.format(counter, tracking))

    if not position == ():
        x,y = position

        selection = cv2.getRectSubPix(img, (50, 50), (x, y))
        cv2.imshow('selection',selection)

        if tracking == False:
            cv2.putText(img, 'Not Tracking', (75,75), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2)
            #print('in selection loop')
            hsv = cv2.cvtColor(selection, cv2.COLOR_BGR2HSV)
            hue, saturation, value = cv2.split(hsv)
            
            h = np.mean(hue)
            s = np.mean(saturation)
            v = np.mean(value)
            h_std = np.std(hue)
            s_std  = np.std(saturation)
            v_std  = np.std(value)

            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            upper =  np.array([int(h+2*h_std), int(s+2*s_std), int(v+2*v_std)])
            lower =  np.array([int(h-2*h_std), int(s-2*s_std), int(v-2*v_std)])

            blobs = cv2.inRange(cv2.GaussianBlur(hsv, (11,11), 1), lower, upper)
            element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15), (7, 7))
            blobs = cv2.erode(blobs, element)
            element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13), (6, 6))
            blobs = cv2.dilate(blobs, element)

            contours, hierarchy = cv2.findContours(blobs, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # Get the moments
            mu = [None]*len(contours)
            for i in range(len(contours)):
                mu[i] = cv2.moments(contours[i])
            # Get the mass centers
            mc = [None]*len(contours)
            for i in range(len(contours)):
                # add 1e-5 to avoid division by zero
                mc[i] = (mu[i]['m10'] / (mu[i]['m00'] + 1e-5), mu[i]['m01'] / (mu[i]['m00'] + 1e-5))
            # Draw contours
            
            drawing = np.zeros((blobs.shape[0], blobs.shape[1], 3), dtype=np.uint8)
            
            maxArea = 0
            maxContour = None
            for i in range(len(contours)):
                area = cv2.contourArea(contours[i])
                xb,yb,wb,hb = cv2.boundingRect(contours[i])
                if xb < x and x < xb+wb and yb < y and y < yb + hb:
                    if area > 100 and area > maxArea:
                        maxArea = area
                        maxContour = i

            if not maxContour == None:
                color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
                cv2.drawContours(drawing, contours, maxContour, color, 2)
                cv2.circle(drawing, (int(mc[maxContour][0]), int(mc[maxContour][1])), 4, color, -1)
                xb,yb,wb,hb = cv2.boundingRect(contours[maxContour])
                #cv2.rectangle(img,(xb,yb),(xb+wb,yb+hb),(0,255,0),2)
                counter += 1
                display_boxes.append((xb,yb,wb,hb))
                display_scores.append(1.0)

            cv2.imshow('Contours', drawing)
            cv2.imshow('blobs',blobs)

            # if display_boxes != [] and counter % 10 == 0:
            if len(display_boxes) == 10:
                index = cv2.dnn.NMSBoxes(display_boxes, display_scores, score_threshold=0.5, nms_threshold=0.3, top_k=1)
                #print(index)
                #print(display_boxes)
                display_box = display_boxes[index[0][0]]
                display_boxes = []
                display_scores = []
                tracking = True
                xb,yb,wb,hb = display_box
                print('ROI: x:{} y:{} w:{} h:{}'.format(xb,yb,wb,hb))
                print("start tracking: {}".format(tracking))
                tracker = cv2.TrackerCSRT_create()
                bbox = display_box
                tracker.init(img, bbox)

        elif tracking == True:
            success, bbox = tracker.update(img)

            if success:
                cv2.putText(img, 'Tracking', (75,75), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,255,0),2)
                display_box = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))
                
                margin = 50
                #print(bbox[0])
                xc = bbox[0] + bbox[2]/2
                yc = bbox[1] + bbox[3]/2
                if xc < frame_w/2 - margin:  
                    #print('move left')
                    cv2.arrowedLine(img, (50,int(frame_h/2)), (10,int(frame_h/2)), (0,255,0), 5, tipLength = 0.3)
                elif xc > frame_w/2 + margin:  
                    #print('move right')
                    cv2.arrowedLine(img, (frame_w - 50,int(frame_h/2)), (frame_w - 10,int(frame_h/2)), (0,255,0), 5, tipLength = 0.3)
                if yc < frame_h/2 - margin:  
                    #print('move down')
                    cv2.arrowedLine(img, (int(frame_w/2),50), (int(frame_w/2),10), (0,255,0), 5, tipLength = 0.3)
                elif yc > frame_h/2 + margin:  
                    #print('move up')
                    cv2.arrowedLine(img, (int(frame_w/2),frame_h - 50), (int(frame_w/2),frame_h - 10), (0,255,0), 5, tipLength = 0.3)

            else:
                cv2.putText(img, 'Not Tracking', (75,75), cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0,0,255),2)


    if display_box != None:
        xb,yb,wb,hb = display_box
        cv2.rectangle(img,(xb,yb),(xb+wb,yb+hb),(0,255,0),2)    
    cv2.imshow('image',img)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break

    