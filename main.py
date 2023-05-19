import cv2 as cv
import os
from cvzone.HandTrackingModule import HandDetector
img_list = os.listdir("Slides")
print(img_list)
i = 0
slide = cv.imread("Slides/"+img_list[i])
slide = cv.resize(slide,(800,600))
v = cv.VideoCapture(0)
detector = HandDetector(maxHands = 2, detectionCon=0.8)
while True:
    ret,frame = v.read()
    flipped_frame = cv.flip(frame,1)  #flips horizontally
    cv.line(flipped_frame,(0,250),(800,250),(0,255,0),1)
    hands,flipped_frame = detector.findHands(flipped_frame)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
                
    small_v = cv.resize(flipped_frame,(150,100))
    cv.imshow("frame",flipped_frame);
    y = slide.shape[0] - small_v.shape[0] - 10   
    x = slide.shape[1] - small_v.shape[1] - 10   
    slide[y:y+small_v.shape[0],x:x+small_v.shape[1]] = small_v    # Selecting the region on the background image for placing video. 
    key = cv.waitKey(1)
    cv.imshow("1",slide)
    if key==ord('q'):
        break

v.release()
cv.destroyAllWindows()