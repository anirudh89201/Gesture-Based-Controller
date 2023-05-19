import cv2 as cv
import os
from cvzone.HandTrackingModule import HandDetector
img_list = os.listdir("Slides")
print(img_list)
i = 0
slide = cv.imread("Slides/"+img_list[i])
slide = cv.resize(slide,(800,600))
v = cv.VideoCapture(0)

detector = HandDetector(maxHands = 1, detectionCon=0.8)

while True:
    
    ret,frame = v.read()
    flipped_frame = cv.flip(frame,1)  #flips horizontally
    hands,flipped_frame = detector.findHands(flipped_frame)
    small_v = cv.resize(flipped_frame,(150,100))
    y = slide.shape[0] - small_v.shape[0] - 10   
    x = slide.shape[1] - small_v.shape[1] - 10   
    slide[y:y+small_v.shape[0],x:x+small_v.shape[1]] = small_v    # Selecting the region on the background image for placing video. 
    key = cv.waitKey(1)
    cv.imshow("1",slide)
    if key==ord('q'):
        break

v.release()
cv.destroyAllWindows()