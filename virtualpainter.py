import cv2
import numpy as np
import os
import time
import handtrackingmodule as htm

brushthickness=10
erasorthickness=50


folderpath="header"
mylist=os.listdir(folderpath)
print(mylist)
overlaylist=[]

for impath in mylist:
    image=cv2.imread(f'{folderpath}/{impath}')
    overlaylist.append(image)
print(len(overlaylist))

header=overlaylist[0]
drawcolor=(255,0,255)


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector=htm.handDetector(detectioncon=0.85)
xp,yp=0,0
imgcanvas=np.zeros((480,640,3),np.uint8)

while True:
    # 1.import images
    sucess,img = cap.read()
    img=cv2.flip(img,1)#for right side move to right side

    # 2. fing hand landmark
    img=detector.findHand(img)
    lmlist=detector.findposition(img,draw=False)

    if len(lmlist)!=0:
        #print(lmlist)

        #tip of index fingre
        x1, y1 = lmlist[8][1:]
        x2,y2=lmlist[12][1:]



    # 3. checking which fingres are up

        fingres=detector.fingresup()
        #print(fingres)

    # 4. if selection mode:2 fingres are up then we have to select not draw
        if fingres[1] and fingres[2]:

            #checking for the click
            if y1<62:
                if 125<x1<200:
                    header=overlaylist[0]
                    drawcolor=(255,0,255)
                elif 220<x1<320:
                    header = overlaylist[1]
                    drawcolor = (0, 255,0)
                elif 350<x1<450:
                    header = overlaylist[2]
                    drawcolor = (255, 0, 0)
                elif 470<x1<590:
                    header = overlaylist[3]
                    drawcolor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)
            #print("selection mode")

    # 5.drawing mode: index fingre is up
        if fingres[1] and fingres[2]== False:
            cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
            print("drawing mode")
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawcolor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, erasorthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, erasorthickness)
            else:
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, brushthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, brushthickness)




            xp,yp=x1,y1






    # setting the header image
    img[0:64,0:640]=header
    cv2.imshow("image",img)
    cv2.imshow("canvas", imgcanvas)
    cv2.waitKey(1)