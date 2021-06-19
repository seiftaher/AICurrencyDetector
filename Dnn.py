import cv2
import numpy as np

#Reading the trained YOLOv3 dnn 
net = cv2.dnn.readNet('yolov3_training_last.weights', 'yolov3_testing.cfg')

#Defining the multi classes which are 1EG, 50Piasters, 25Piasters,
#2Euro, 1Euro, 50Cents, 20Cents, 10Cents, 5Cents, 2Cents, 1Cent
classes = []
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()

#setting the font and randomizing the colors for drawn boxes in the output image
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

#Function responsible for prediction and drawing boundary box around the coin
def predict(img):
  height, width, _ = img.shape

  #Predicting the input image using the defined dnn and saving the indices of the output layers
  blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
  net.setInput(blob)
  output_layers_names = net.getUnconnectedOutLayersNames()
  layerOutputs = net.forward(output_layers_names)

  boxes = []
  confidences = []
  class_ids = []

  #Getting the maximum score of output classes and set it as the predicted class
  for output in layerOutputs:
      for detection in output:
          scores = detection[5:]
          class_id = np.argmax(scores)
          
          #Defining boundary box parameters for drawing if the score of the class is higher than 25%
          confidence = scores[class_id]
          if confidence > 0.25:
              center_x = int(detection[0]*width)
              center_y = int(detection[1]*height)
              w = int(detection[2]*width)
              h = int(detection[3]*height)

              x = int(center_x - w/2)
              y = int(center_y - h/2)

              boxes.append([x, y, w, h])
              confidences.append((float(confidence)))
              class_ids.append(class_id)

  indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.4)
  
  #Drawing the boundary box around the predicted coin
  #with a label with the name of the class inside
  if len(indexes)>0:
      for i in indexes.flatten():
          x, y, w, h = boxes[i]
          label = str(classes[class_ids[i]])
          confidence = str(round(confidences[i],2))
          color = colors[i]
          cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
          if not label:
            return
          cv2.putText(img, label[:-1], (x, y+20), font, 2, (0,255,0), 2)
  try:
    print (label,"  ", confidence)
    return label
  except:
    return
