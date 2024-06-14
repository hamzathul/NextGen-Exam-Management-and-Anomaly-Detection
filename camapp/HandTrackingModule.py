import datetime

from DBConnection import Db

ms = 0
import mediapipe as mp

import cv2
import numpy as np
import uuid
import os
db=Db()
hallid = 1
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
joint_list = [[8, 5, 0]]
tipIds = [4, 8, 12, 16, 20]
mpath="C:\\Users\\prana\\PycharmProjects\\exam"

totalFingers = 0


def draw_finger_angles(image, results, joint_list):
    for hand in results.multi_hand_landmarks:

        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])  # First coord
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])  # Second coord
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])  # Third coord

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            cv2.putText(image, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    return image, angle


def get_label(index, hand, results):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label, round(score, 2))

            coords = tuple(np.multiply(
                np.array(
                    (hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                [640, 480]).astype(int))

            output = text, coords

    return output


cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = cv2.flip(image, 1)

        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:

            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                 circle_radius=2),
                                          )

                if get_label(num, hand, results):
                    text, coord = get_label(num, hand, results)
                    cv2.putText(image, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            image, angle = draw_finger_angles(image, results, joint_list)

            lmList = []
            for id, lm in enumerate(hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            fingers = []

            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):

                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            # print(totalFingers, hand)



            # print(totalFingers, 'fingers')
            # print(angle, totalFingers)
            if angle <= 180:
                if totalFingers == 2:
                    ms = 1
                    # print(ms)

                elif totalFingers == 3:
                    ms = 2
                    # print(ms)
                elif totalFingers == 4:
                    ms = 3
                    # if ms != 5:
                    #     ms = 5
                    # print(ms)
                elif totalFingers == 5:
                    ms = 4
                    # print(ms)
                elif totalFingers == 5:
                # elif totalFingers == 4:

                    if ms != 5:
                        ms = 5
                    # print('angle', angle)
                    # print(ms, 'msss')
            else:
                if totalFingers == 1:
                    ms = 1
                    # print(ms)

                elif totalFingers == 2:
                    ms = 2
                    # print(ms)

                elif totalFingers == 3:
                    ms = 3

                    # print(ms)

                elif totalFingers == 4:
                    ms = 4
                    # print(ms)

                elif totalFingers > 4:

                    # if ms != 5:
                    ms = 5
                    # print('angle', angle, 'else')
                    # print(ms, 'else')

            print(ms)
            if ms>0:
                fname = datetime.datetime.now().strftime("%Y%m%d%H%M%f") + ".jpg"
                p = "/media/" + fname
                cv2.imwrite(mpath+ '\\media\\' + fname, frame)
                text = 'A hand gesture has been detected'
                if ms==1:
                    text = 'A hand gesture with number 1 has been detected'
                if ms==2:
                    text = 'A hand gesture with number 2 has been detected'
                if ms==3:
                    text = 'A hand gesture with number 3 has been detected'
                if ms==4:
                    text = 'A hand gesture with number 4 has been detected'
                if ms==5:
                    text = 'A hand gesture with number 5 has been detected'
                qry = "INSERT INTO myapp_abnormalactivity (DATE, TIME, TYPE, CONTENT, PHOTO, hall_id) VALUES (CURDATE(), CURTIME(), 'hand gesture', '" + text + "','" + p + "','" + str(
                    hallid) + "')"
                db.insert(qry)

            # if angle <= 180:
            #     print(totalFingers)
            # else:
            #     print(totalFingers)

cap.release()
cv2.destroyAllWindows