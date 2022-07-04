import cv2
import numpy as np

#@@@@@@@@@@@@@@@@@@@ Class-LABELS 
# load the COCO class labels our YOLO model was trained on
labelsPath = '/Users/dhimant/Desktop/Project/coco.names'
LABELS = open(labelsPath).read().strip().split("\n")
# initialize a list of colors to represent each possible class label
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")


net1=cv2.dnn.readNet("/Users/dhimant/Desktop/Project/custom-yolov4-detector_best.weights","/Users/dhimant/Desktop/Project/custom-yolov4-detector.cfg")
cal=[]
with open("/Users/dhimant/Desktop/all/Programs/coco.names","r") as f:
    cal=f.read().splitlines()

cap=cv2.VideoCapture(1)

#########################################################################################
#ADD ON TO SAVE THE VIDEO
width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
size = (width,height)

out = cv2.VideoWriter('sample_output001.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 25, size)
###ADD ON TO SAVE THE VIDEO----->END




while True:
    _, img1=cap.read()
    height,width=img1.shape[:2]

    blob=cv2.dnn.blobFromImage(img1,1/255,(416,416),(0,0,0),swapRB=True,crop=False)
    net1.setInput(blob)

    output_layers=net1.getUnconnectedOutLayersNames()
    layerOutputs=net1.forward(output_layers)

    boxes=[]
    confidences=[]
    class_id=[]
    classIDs = []

    for output in layerOutputs:
        for detection in output:
            scores=detection[5:]
            class_id=np.argmax(scores)
            confidence=scores[class_id]
            if confidence >0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                classIDs.append(class_id)

        
        
        
    indexes=cv2.dnn.NMSBoxes(boxes,confidences,0.3,0.4)

    font=cv2.FONT_HERSHEY_PLAIN
    colors=(0,255,0)
    if len(indexes) > 0:
        for i in indexes.flatten():
            x,y,w,h=boxes[i]
            label="CAR"
            confidence=str(round(confidences[i],2))
            color=(0,255,0)
            cv2.rectangle(img1,(x,y),(x+w,y+h),color,2)
            cv2.putText(img1,label+" "+confidence,(x,y+20),font,1,(255,255,255),4)

            color = (0,255,0)
            cv2.rectangle(img1, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(img1, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2) 

    #END1111111111111111111111111!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    cv2.waitKey(2000)
    # out.write(img1)
    cv2.imshow("feed", img1)

    #cv2.imshow("Result",img1)  
    key=cv2.waitKey(1)
    if key==27:
        break
cap.release()    
cv2.destroyAllWindows()