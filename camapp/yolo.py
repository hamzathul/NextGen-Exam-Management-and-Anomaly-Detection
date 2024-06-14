import datetime

from PIL import Image
import numpy as np
import cv2

from DBConnection import Db

classes_names = ['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
                 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake',
                 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet', 'tvmonitor', 'laptop', 'mouse',
                 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
                 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
model = cv2.dnn.readNet(r"C:\Social-Distancing-Detection-in-Real-Time-main\yolo\yolov3.cfg",r"C:\Social-Distancing-Detection-in-Real-Time-main\yolo\yolov3.weights")
layer_names = model.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]
output_layers = [layer_names[i-1] for i in model.getUnconnectedOutLayers()]
# output_layers = [layer_names[i-1] for i in model.getUnconnectedOutLayers()]
db=Db()
hallid=1

mpath="C:\\Users\\prana\\PycharmProjects\\exam"

def check(path):

    image = Image.open(path)
    div = image.size[0] / 500
    resized_image = image.resize((round(image.size[0] / div), round(image.size[1] / div)))
    resized_image.save('C:\\Social-Distancing-Detection-in-Real-Time-main\\na.jpg')
    image = cv2.imread("C:\\Social-Distancing-Detection-in-Real-Time-main\\na.jpg")
    height, width, channels = image.shape
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    model.setInput(blob)
    outputs = model.forward(output_layers)
    class_ids = []
    confidences = []
    boxes = []
    for output in outputs:
        for identi in output:
            scores = identi[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.8:
                class_ids.append(class_id)

    if 63 in class_ids and 67 in class_ids:
        fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
        p = "/media/" + fname
        cv2.imwrite(mpath + '\\media\\' + fname, image)
        qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'object detected', 'laptop and cell phone nearby','" + p + "','" + str(
            hallid) + "')"
        db.insert(qry)

        return "cell phone and laptop nearby"
    elif 67 in class_ids:
        fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
        p = "/media/" + fname
        cv2.imwrite(mpath + '\\media\\' + fname, image)
        qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'object detected', 'cell phone found','" + p + "','" + str(
            hallid) + "')"
        db.insert(qry)
        return "cell phone found"

    elif 63 in class_ids:

        fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
        p = "/media/" + fname
        cv2.imwrite(mpath + '\\media\\' + fname, image)
        qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'object detected', 'laptop found','" + p + "','" + str(
            hallid) + "')"
        db.insert(qry)
        return "laptop found"
    else:
        return "no"
