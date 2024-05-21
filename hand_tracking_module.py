import cv2
import mediapipe as mp


class HandTracking:
    # on start this function will build
    def __init__(self, mode=False, numHands=2, complex=1, detectionConf=0.5, trackingConf=0.5):
        self.mode = mode
        self.numHands = numHands
        self.complex = complex
        self.detectionConf = detectionConf
        self.trackingConf = trackingConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.numHands, self.complex, self.detectionConf, self.trackingConf)
        self.mpDraw = mp.solutions.drawing_utils  # draw var

    def find_hands(self, img, draw=True):

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)  # this var contain all data we need
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)  # if i want to draw in the hand
        return img

    def which_hand(self):
        handedness = self.results.multi_handedness  # return map to left and right hand
        # print(handedness)
        return handedness

    def find_position(self, img, hand_no=0):
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(myhand.landmark):
                # lm contain the x ,y and z for each point of hand in decimal not in pixel
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), lm.z
                self.lm_list.append([id, cx, cy, cz])

            return self.lm_list

    def which_finger_up(self, img):

        point_list = [4, 8, 12, 16, 20]
        finger_statu = []

        # detect which hand to detect the right thumb position
        handedness = self.which_hand()
        hand_label = handedness[0].classification[-1].label

        thumb_tip = self.lm_list[point_list[0]][1]
        thumb_ip = self.lm_list[point_list[0] - 1][1]
        index_finger_tip = self.lm_list[point_list[1]][1]
        # Right Hand and camera look to hand bottom
        if hand_label == "Right" and thumb_tip < index_finger_tip:
            if thumb_tip < thumb_ip:
                finger_statu.append(1)
            else:
                finger_statu.append(0)

        # Right Hand and camera look to hand face
        elif hand_label == "Right" and thumb_tip < index_finger_tip:
            if thumb_tip > thumb_ip:
                finger_statu.append(1)
            else:
                finger_statu.append(0)

        # Left Hand and camera look to hand face
        elif hand_label == "Left" and thumb_tip < index_finger_tip:
            if thumb_tip < thumb_ip:
                finger_statu.append(1)
            else:
                finger_statu.append(0)

        # Left Hand and camera look to hand bottom
        else:
            if thumb_tip > thumb_ip:
                finger_statu.append(1)
            else:
                finger_statu.append(0)

        # detect  other fingers to detect the right position
        for i in range(1, 5):
            if self.lm_list[point_list[i]][2] < self.lm_list[point_list[i] - 2][2]:
                finger_statu.append(1)
            else:
                finger_statu.append(0)

        return finger_statu




































# def main():
#     # code in this function we can use it other file,but we should import the "hand_tracking_module"
#     # it is a dummy code for test
#     cap = cv2.VideoCapture(0)
#     detector = HandTracking()
#     sign = {"0,1,1,1,1": "Hello", "0,0,0,0,0": "Yes", "1,1,0,0,1": "i love you"}
#     while True:
#         success, img = cap.read()
#         img = detector.find_hands(img)
#         lm_list = detector.find_position(img)
#         # print(lm_list)
#         if lm_list is not None:
#
#             finger_statu = detector.which_finger_up(img)
#             # print(str(finger_statu)[1:-1].replace(" ","").split(","))
#             # print(sign[str(finger_statu)])
#             # print(sign.keys())
#             for s in sign.keys():
#                 # print( s.split(","))
#                 if s.split(",") == str(finger_statu)[1:-1].replace(" ", "").split(","):
#                     cv2.putText(img, sign[str(finger_statu)[1:-1].replace(" ", "")], (10, 70), cv2.FONT_HERSHEY_DUPLEX,
#                                 3, (255, 0, 0), 2)
#
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if __name__ == "__main__":
#     main()
