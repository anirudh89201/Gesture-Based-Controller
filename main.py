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
lineThreshold = 250
while True:
    ret,frame = v.read()
    flipped_frame = cv.flip(frame,1)  #flips horizontally
    cv.line(flipped_frame,(0,lineThreshold),(800,lineThreshold),(0,255,0),1)
    hands,flipped_frame = detector.findHands(flipped_frame)
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
        cx,cy = hand['center']
        if cy <= lineThreshold:
            if fingers == [1,0,0,0,0]:
                # print('Left')
                if i>0:
                    i-=1 

                    # print(i)
                    slide = cv.imread("Slides/"+img_list[i])
                    slide = cv.resize(slide,(800,600))
            
                else:
                    print("This is the beginning slide of this presentation.")
                
            if fingers == [0,0,0,0,1]:
                # print('Right')
                if i< len(img_list)-1:
                    i+=1 
                    slide = cv.imread("Slides/"+img_list[i])
                    slide = cv.resize(slide,(800,600))
                else:
                    print("This is the end of the presentation.")
                

                
    small_v = cv.resize(flipped_frame,(150,100))
    # cv.imshow("frame",flipped_frame);
    y = slide.shape[0] - small_v.shape[0] - 10   
    x = slide.shape[1] - small_v.shape[1] - 10   
    slide[y:y+small_v.shape[0],x:x+small_v.shape[1]] = small_v    # Selecting the region on the background image for placing video. 
    key = cv.waitKey(1)
    cv.imshow("Presentation Slides",slide)
    if key==ord('q'):
        break

v.release()
cv.destroyAllWindows()