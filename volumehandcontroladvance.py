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
area=0
colvol=(255,0,0)

detector=htm.handDetector(detectioncon=0.5,maxHands=1)

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
    lmList, bbox = detector.findposition(img, draw=True)
    if len(lmList) != 0:
      #print(bbox)
      area=(bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
      #print(area)
      if 250<area<1000:
          #print('yes')

          #find distance between index and thumb
          length, img, lineinfo = detector.findDistance(4, 8, img)
          #print(length)
          #len,img,info=detector.findDistance(8,4,img)

          #convert volume
          #vol = np.interp(length, [50, 300], [minvol, maxvol])
          volbar=np.interp(length, [50, 300], [400, 150])
          volper=np.interp(length, [50, 300], [0, 100])

          smoothness=10
          volper=smoothness*round(volper/smoothness)

          #fingrres up
          fingres=detector.fingresup()

          #fingers = detector.fingersUp()
          print(fingres)


          if not fingres[4]:
          #volume.SetMasterVolumeLevel(vol, None)
           volume.SetMasterVolumeLevelScalar(volper/100,None)
           cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
           colvol=(0,255,0)
          else:
              colvol = (255, 0, 0)




          cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
          cv2.rectangle(img, (50, int(volbar)), (85, 400), (255, 0, 0), cv2.FILLED)
          cv2.putText(img, f'{int(volper)}%', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 8, 8), 3)
          cvol=int(volume.GetMasterVolumeLevelScalar()*100)
          cv2.putText(img, f'vol set: {str(int(cvol))}', (400, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, colvol, 3)






         #hand range:50-300
         #volrange:-128 to -127


          #print(int(length),vol)



          #if length<=20:
              #cv2.circle(img, (lineinfo[4], lineinfo[5]), 15, (0, 255, 0), cv2.FILLED)
    #drawings




    #fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    #putting fps as text on img
    #cv2.putText(img,f'FPS: {str(int(fps))}', (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 8, 8), 3)
    cv2.imshow("Img",img)
    cv2.waitKey(1)