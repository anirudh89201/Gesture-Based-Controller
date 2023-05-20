import cv2 as cv
import os
import numpy as np
from cvzone.HandTrackingModule import HandDetector

width, height = 800, 600

img_list = os.listdir("Slides")
print(img_list)
i = 0
slide = cv.imread("Slides/"+img_list[i])
slide = cv.resize(slide,(800,600))
v = cv.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
lineThreshold = 250

clickCounter = 0 
clickLimit = 5
clickCheck = False


while True:
    ret,frame = v.read()
    flipped_frame = cv.flip(frame,1)  #flips horizontally
    cv.line(flipped_frame,(0,lineThreshold),(800,lineThreshold),(0,255,0),1)
    hands,flipped_frame = detector.findHands(flipped_frame)
    
    cv.imshow("Cam", flipped_frame)
    if cv.waitKey(1) & 0xFF == ord("q"):
                break
    
    if hands and clickCheck==False:

        
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)


        cx,cy = hand['center']

        lmList = hand["lmList"]  # for pointer and drawing
        # Setting the pointer movement on the right hand side
        xvalue = int(np.interp(lmList[8][0], [300, 750], [0, 800]))
        yvalue = int(np.interp(lmList[8][1], [50, 500], [0, 600]))
        indexFinger = xvalue, yvalue

        if cy <= lineThreshold:
            if fingers == [1,0,0,0,0]:
                clickCheck = True
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
                    clickCheck = True
                    i+=1 
                    slide = cv.imread("Slides/"+img_list[i])
                    slide = cv.resize(slide,(800,600))
                else:
                    print("This is the end of the presentation.")
            

            # Pointer
        if fingers == [0, 1, 1, 0, 0]:
            x = fingers[1] * slide.shape[1]
            y = fingers[2] * slide.shape[0]
            # cv.circle(slide, indexFinger, 12, (0, 0, 255), cv.FILLED)
            cv.circle(slide, indexFinger, 12, (0, 0, 255), cv.FILLED)

    cv.imshow("Presentation slides", slide)

    if clickCheck:
        clickCounter+=1 
        if clickCounter > clickLimit:
            clickCounter = 0 
            clickCheck = False 
                

                
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
