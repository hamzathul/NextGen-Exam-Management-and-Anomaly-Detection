from mylib import config, thread
from mylib.mailer import Mailer
from mylib.detection import detect_people


import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)


from imutils.video import VideoStream, FPS
from scipy.spatial import distance as dist
import numpy as np
import argparse, imutils, cv2, os, time
import cv2
import numpy as np

import pyttsx3
from keras.models import load_model

####loading emotion model
from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense

from yolo import check

model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.load_weights(r'C:\Social-Distancing-Detection-in-Real-Time-main\emotionmodel\model.h5')

# prevents openCL usage and unnecessary logging messages
cv2.ocl.setUseOpenCL(False)

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

facecasc = cv2.CascadeClassifier(
    r'C:\Social-Distancing-Detection-in-Real-Time-main\emotionmodel\haarcascade_frontalface_default.xml')


def emo_check( frame):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    p=""
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        maxindex = int(np.argmax(prediction))
        print(emotion_dict[maxindex])
        p=emotion_dict[maxindex]
        return  p

    return p


###end loading emotion model


####function detect pose of a person by photo
from keras.models import load_model


def inFrame(lst):
    if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility>0.6 and lst[16].visibility>0.6:
        return True
    return False


model1 = load_model(
    r"C:\Social-Distancing-Detection-in-Real-Time-main\posemodel\model.h5")

holistic = mp.solutions.pose
holis = holistic.Pose()
drawing = mp.solutions.drawing_utils

def detect_position(frm):
    label = np.load(r"C:\Social-Distancing-Detection-in-Real-Time-main\posemodel\labels.npy")
    def inFrame(lst):
        if lst[28].visibility > 0.6 and lst[27].visibility > 0.6 and lst[15].visibility > 0.6 and lst[16].visibility > 0.6:
            return True
        return False

    frm = cv2.flip(frm, 1)
    res = holis.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))
    frm = cv2.blur(frm, (4, 4))
    lst=[]
    if res.pose_landmarks and inFrame(res.pose_landmarks.landmark):
        for i in res.pose_landmarks.landmark:
            lst.append(i.x - res.pose_landmarks.landmark[0].x)
            lst.append(i.y - res.pose_landmarks.landmark[0].y)

        lst = np.array(lst).reshape(1, -1)
        p = model1.predict(lst)
        pred = label[np.argmax(p)]
        if p[0][np.argmax(p)] > 0.75:
            print(p[0][np.argmax(p)], "score")

            # db.instoreport("Posture", "Detected posture is"+ pred)

            print("Posture", "Detected posture is"+ pred)

            print(pred, "result")
        else:
            print(pred, "result")
    else:
        print('body not visible')


####end function detect pose of a person by photo
####face landmark loading of students

print("Student face land mark extraction started")
from DBConnection import Db
db=Db()
import face_recognition
qry="select * from myapp_student"
res=db.select(qry)
mpath="C:\\Users\\prana\\PycharmProjects\\exam"
hallid=1
knownimage=[]
knownids=[]
knownsems=[]

for i in res:
    s=i['photo']
    s=s.replace("/","\\")
    pth=mpath+ s
    picture_of_me = face_recognition.load_image_file(pth)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]
    knownimage.append(my_face_encoding)
    knownids.append(i['id'])
    knownsems.append(str(i['name']))

print("Student face land mark extraction ended")
print("total extracted landmarks=" ,len(knownids), "They are", knownids)
####face landmark loading end

labelsPath = "C:\\Social-Distancing-Detection-in-Real-Time-main\\yolo\\coco.names"
LABELS = open(labelsPath).read().strip().split("\n")

weightsPath = "C:\\Social-Distancing-Detection-in-Real-Time-main\\yolo\\yolov3.weights"
configPath = "C:\\Social-Distancing-Detection-in-Real-Time-main\\yolo\\yolov3.cfg"
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

if config.USE_GPU:

    print("[INFO] Looking for GPU")
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

cap = cv2.VideoCapture(0)

person_count=0
writer = None

fps = FPS().start()
totalcount=0

while True:

    try:
        ret,frame = cap.read()
        cv2.imwrite("fram.jpg",frame)
        m=check("fram.jpg")
        print("Checked result",m)
        if m!="no":
            # db.instoreport("object deteted",m)

            print("object deteted",m)

        frame = imutils.resize(frame, width=700)
        results,totalcountnew = detect_people(frame, net, ln,
            personIdx=LABELS.index("person"))

        if int(totalcountnew) > totalcount:
            print("Person entry", str((totalcountnew - totalcount)) + "Person entered to room")############################################################
            import datetime

            fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
            p = "/media/" + fname
            cv2.imwrite(mpath + '\\media\\' + fname, frame)
            qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'person entry', '"+ str((totalcountnew - totalcount)) + "Person entered to room" +" ','" + p + "','" + str(
                hallid) + "')"
            db.insert(qry)

            # db.instoreport("Person entry" ,str((totalcountnew-totalcount)) + "Person entered to room")
            totalcount=totalcountnew

        serious = set()
        abnormal = set()

        if len(results) >= 2:

            centroids = np.array([r[2] for r in results])
            D = dist.cdist(centroids, centroids, metric="euclidean")

            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):

                    if D[i, j] < config.MIN_DISTANCE:

                        serious.add(i)
                        serious.add(j)

                    if (D[i, j] < config.MAX_DISTANCE) and not serious:
                        abnormal.add(i)
                        abnormal.add(j)

        for (i, (prob, bbox, centroid)) in enumerate(results):
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)
            if i in serious:
                color = (0, 0, 255)
            elif i in abnormal:
                color = (0, 255, 255) #orange = (0, 165, 255)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.circle(frame, (cX, cY), 5, color, 2)
            if (endY- startY > 0 ) and  (endX-startX > 0):

                try:
                    crop = frame[startY:endY,startX:endX]
                    results = face_mesh.process(crop)
                    print(results)
                    crop.flags.writeable = True
                    # Convert the color space from RGB to BGR
                    image = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)
                    img_h, img_w, img_c = crop.shape
                    face_3d = []
                    face_2d = []
                    if results.multi_face_landmarks:
                        for face_landmarks in results.multi_face_landmarks:
                            for idx, lm in enumerate(face_landmarks.landmark):
                                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                                    if idx == 1:
                                        nose_2d = (lm.x * img_w, lm.y * img_h)
                                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)
                                    x, y = int(lm.x * img_w), int(lm.y * img_h)
                                    # Get the 2D Coordinates
                                    face_2d.append([x, y])
                                    # Get the 3D Coordinates
                                    face_3d.append([x, y, lm.z])
                                    # Convert it to the NumPy array
                            face_2d = np.array(face_2d, dtype=np.float64)
                            # Convert it to the NumPy array
                            face_3d = np.array(face_3d, dtype=np.float64)
                            focal_length = 1 * img_w
                            cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                                   [0, focal_length, img_w / 2],
                                                   [0, 0, 1]])
                            dist_matrix = np.zeros((4, 1), dtype=np.float64)
                            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                            rmat, jac = cv2.Rodrigues(rot_vec)
                            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)
                            x = angles[0] * 360
                            y = angles[1] * 360

                            if y < -20:
                                text = "Looking Right"

                                import datetime

                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath+'\\media\\' + fname, frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'pose', '" + text + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)



                                print(text)
                            elif y > 20:
                                from datetime import datetime
                                print("Looking Left")

                                import datetime
                                text="Looking Left"

                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath+'\\media\\' + fname, frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'pose', '" + text + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)
                            elif x < -5:
                                from datetime import datetime

                                import datetime

                                text = "Looking down"

                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath+'\\media\\' + fname, frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'pose', '" + text + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)
                                print("Looking down")
                            elif x> 5:
                                print("Looking upward")
                                text = "upward"

                                import datetime

                                text = "Looking upward"

                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath+'\\media\\' + fname, frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'pose', '" + text + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)
                                print(text)


                    cv2.imwrite("a.jpg",crop)
                    picture_of_others = face_recognition.load_image_file("a.jpg")
                    others_face_encoding = face_recognition.face_encodings(picture_of_others)
                    totface = len(others_face_encoding)
                    print("In face detection, Detected face count is", totface)
                    print("recognizing posture")
                    detect_position(crop)
                    for i in range(0, totface):
                        res = face_recognition.compare_faces(knownimage, others_face_encoding[i], tolerance=0.5)
                        if True in res:
                            print('found ', knownids[res.index(True)], knownsems[res.index(True)])
                            print("recognizing emotion")
                            em = emo_check(frame)
                            if em != "":
                                print("========lk")
                                print(em)

                                import datetime
                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath+'\\media\\'+fname,frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'emotion', '" + em + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)


                        else:
                            print()
                            # db.instoreport("unknown person","An unknown person in class")

                            print("unknown person","An unknown person in class")
                            import datetime

                            fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                            p = "/media/" + fname
                            cv2.imwrite(mpath + '\\media\\' + fname, frame)
                            qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'person', 'An unknown person in class ','" + p + "','" + str(
                                hallid) + "')"
                            db.insert(qry)

                            em = emo_check(frame)

                            if em!="" and em!="no":
                                print("pass")

                                import datetime

                                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                                p = "/media/" + fname
                                cv2.imwrite(mpath +'\\media\\' + fname, frame)
                                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'person', '" +  "Emotion of unknown perosn "+ " is " + str(em) + "','" + p + "','" + str(
                                    hallid) + "')"
                                db.insert(qry)

                                # db.instoreport("emotion", "Emotion of unknown perosn "+ " is " + str(em))

                            person_count = person_count + 1

                        l = 0
                except Exception as a:
                    print("errrror",a)
                    pass
        cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("q"):
            break
        fps.update()
    except:
        pass
fps.stop()
cv2.destroyAllWindows()
