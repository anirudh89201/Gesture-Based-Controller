import cv2 as cv
import numpy as np
import os
from cvzone.HandTrackingModule import HandDetector
img_list = os.listdir("Slides")
print(img_list)
i = 0
slide = cv.imread("Slides/"+img_list[i])
width,height = 800,600
slide = cv.resize(slide,(width,height))
# slide = cv.resize(slide,cap.set)
v = cv.VideoCapture(0)
detector = HandDetector(maxHands = 1, detectionCon=0.8)
lineThreshold = height//3

# clickCounter = 0 
# clickLimit = 5
# clickCheck = False
annotations = [[]]
annotationStart = False 
annotationCount = -1
while True:
    ret,frame = v.read()
    flipped_frame = cv.flip(frame,1)  #flips horizontally
    cv.line(flipped_frame,(0,lineThreshold),(width,lineThreshold),(0,255,0),1)
    hands,flipped_frame = detector.findHands(flipped_frame)
    # if hands and clickCheck==False:
    v_width , v_height = 150,100
    small_v = cv.resize(flipped_frame,(v_width,v_height))
    # cv.imshow("frame",flipped_frame);
    y = slide.shape[0] - small_v.shape[0] - 10   
    x = slide.shape[1] - small_v.shape[1] - 10   
    slide[y:y+small_v.shape[0],x:x+small_v.shape[1]] = small_v    # Selecting the region on the background image for placing video. 
    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)
        print(fingers)
        cx,cy = hand['center']
        lmlist = hand['lmList']
        # xVal = int(np.interp(lmlist[8][0],[width//2,width],[0,width]))
        # yVal = int(np.interp(lmlist[8][1],[150,height-150],[0,height]))
        xVal = int(np.interp(lmlist[8][0], [width//2, width], [0, width+width]))
        yVal = int(np.interp(lmlist[8][1], [0, height//2], [0, height]))
        indexFinger = xVal,yVal
        if cy <= lineThreshold:
            # clickCheck = True
            if fingers == [1,0,0,0,0]:
                print('Left')

                
                if i>0:
                    i-=1
                    annotations = [[]]
                    annotationStart = False 
                    annotationCount = -1 

                    # print(i)
                    slide = cv.imread("Slides/"+img_list[i])
                    slide = cv.resize(slide,(width,height))
            
                else:
                    print("This is the beginning slide of this presentation.")
                

            if fingers == [0,0,0,0,1]:
                print('Right')
                # clickCheck = True
                if i< len(img_list)-1:
                    i+=1 
                    annotations = [[]]
                    annotationStart = False 
                    annotationCount = -1
                    slide = cv.imread("Slides/"+img_list[i])
                    slide = cv.resize(slide,(width,height))
                else:
                    print("This is the end of the presentation.")
        if fingers == [0,1,1,0,0]:
            cv.circle(slide,indexFinger,5,(0,0,255),cv.FILLED)
        if fingers == [0,1,0,0,0]:
            if annotationStart is False:
                annotationStart = True 
                annotationCount +=1 
                annotations.append([])

            cv.circle(slide,indexFinger,5,(0,0,255),cv.FILLED)
            annotations[annotationCount].append(indexFinger)
        else:
            annotationStart = False 

        if fingers == [0,1,1,1,0]:
            if annotations:
                annotations = [[]]
                annotationStart = False 
                annotationCount = -1 
                slide = cv.imread("Slides/"+img_list[i])
                slide = cv.resize(slide,(width,height))
                # buttonPressed = True

                

        for k in range(len(annotations)):
            for j in range(len(annotations[k])):
                if j!=0:
                    cv.line(slide,annotations[k][j-1],annotations[k][j],(0,255,0),12)
    # if clickCheck:
    #     clickCounter+=1 
    #     if clickCounter > clickLimit:
    #         clickCounter = 0 
    #         clickCheck = False 
                

    key = cv.waitKey(1)
    cv.imshow("Presentation Slides",slide)
    if key==ord('q'):
        break

v.release()
cv.destroyAllWindows()