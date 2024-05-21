import cv2
from hand_tracking_module import HandTracking

cap = cv2.VideoCapture(0)
detector = HandTracking()
sign = {"0,1,1,1,1": "Hello", "0,0,0,0,0": "Yes", "1,1,0,0,1": "i love you"}
while True:
    success, img = cap.read()
    img = detector.find_hands(img)
    lm_list = detector.find_position(img)
    if lm_list is not None:
        finger_statu = detector.which_finger_up(img)
        for s in sign.keys():
            if s.split(",") == str(finger_statu)[1:-1].replace(" ", "").split(","):
                cv2.putText(img, sign[str(finger_statu)[1:-1].replace(" ", "")], (10, 70), cv2.FONT_HERSHEY_DUPLEX,
                            3, (255, 0, 0), 2)
    cv2.namedWindow("IMAGE", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("IMAGE",1280,720)
    cv2.imshow("IMAGE", img)
    cv2.waitKey(1)
































###############################################################################################
# The old code

import cv2
import mediapipe as mp

cap = cv2.VideoCapture("like.jpg")
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
while True:
    _, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    h, w, c = img.shape
    print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
    cv2.namedWindow("IMAGE", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("IMAGE", 1280, 720)
    cv2.imshow("IMAGE", img)
    cv2.imwrite("output.png", img)
    cv2.waitKey(0)











