import cv2
import time
import numpy as np
import handtrackingmodule as htm
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#############################################
wcam,hcam=640,480


#################################################

cap=cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
pTime=0

detector=htm.handDetector(detectioncon=0.7)

#pycow code:

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange=volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)
#print(volrange)

minvol=volrange[0]
maxvol=volrange[1]








while(True):
    sucess,img=cap.read()
    img=detector.findHand(img)
    lmlist=detector.findposition(img,draw=False)
    if len(lmlist)!=0:

      print(lmlist[0],lmlist[8])#thumb and first finger
      x1,y1=lmlist[4][1],lmlist[4][2]
      x2, y2 = lmlist[8][1], lmlist[8][2]
      cx,cy=(x1+x2)//2,(y1+y2)//2

      cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
      cv2.circle(img,(x2,y2), 15, (255, 0, 255), cv2.FILLED)

      cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)


      cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)

      length=math.hypot(x2-x1,y2-y1)
      #print(length)


     #hand range:50-300
     #volrange:-128 to -127

      vol=np.interp(length,[50,300],[minvol,maxvol])
      print(int(length),vol)

      volume.SetMasterVolumeLevel(vol, None)

      if length<=20:
          cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)




    #fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #putting fps as text on img
    cv2.putText(img,f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 8, 8), 3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)