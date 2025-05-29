import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
from time import sleep
import math


def vector_magnitude(vector):
    return math.sqrt(sum(component**2 for component in vector))


def dot_product(v1, v2):
    return sum(
        v1_component * v2_component for v1_component, v2_component in zip(v1, v2)
    )


def rotation_angle(v1, v2):
    dot_product_value = dot_product(v1, v2)
    v1_magnitude = vector_magnitude(v1)
    v2_magnitude = vector_magnitude(v2)
    return math.acos(dot_product_value / (v1_magnitude * v2_magnitude))


cap = cv2.VideoCapture(0)
# Hand Detect
detector = HandDetector(detectionCon=0.8, maxHands=1)
while True:
    success, img = cap.read()
    # img_flip = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=True)
    if hands:
        hand1 = hands[0]
        center1 = hand1["center"]
        lmList = hand1["lmList"]
        x1, y1 = lmList[5][:2]
        x2, y2 = lmList[17][:2]
        x3, y3 = lmList[4][:2]
        x4, y4 = lmList[8][:2]
        x5, y5 = lmList[0][:2]
        position_x, position_y = lmList[9][:2]
        cv2.line(img, (x3, y3), (x4, y4), (0, 255, 0), 5)
        n = 100
        v1 = (n, y5)
        v2 = (x5 - position_x, y5 - position_y)
        cv2.line(img, (x5, y5), (position_x, position_y), (0, 255, 0), 5)
        cv2.line(img, (x5, y5), (n, y5), (0, 255, 0), 5)
        rotation_angle_in_radians = rotation_angle(v1, v2)
        rotation = math.degrees(rotation_angle_in_radians)
        lengthfunc = HandDetector.findDistance(
            img,
            (x1, y1),
            (x2, y2),
            color=(255, 0, 255),
            scale=1,
        )
        fingerDistance = HandDetector.findDistance(
            img,
            (x3, y3),
            (x4, y4),
            color=(255, 0, 255),
            scale=1,
        )
        finger_distance = fingerDistance[0]
        position_z = int(lengthfunc[0])
        position_y = 600 - position_y
        print(position_x, position_y, position_z, finger_distance, rotation)
        sleep(0.0005)
    cv2.imshow("Hand detect", img)
    cv2.waitKey(1)
