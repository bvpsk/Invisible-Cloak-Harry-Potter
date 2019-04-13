import cv2
import numpy as np
import time
import argparse
import glob
import matplotlib.pyplot as plt
cap = cv2.VideoCapture(0)
time.sleep(3)
(grabbed, frame) = cap.read()
fshape = frame.shape
fheight = fshape[0]
fwidth = fshape[1]
print(fwidth , fheight)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (fwidth,fheight))


for i in range(60):
    ret,background = cap.read()
background = np.flip(background,axis = 1)

red_lower1 = np.array([0,120,70])
red_upper1 = np.array([10,255,255])
red_lower2 = np.array([170,120,70])
red_upper2 = np.array([180,255,255])

while cap.isOpened():
    ret,img = cap.read()
    if not ret:
        break
    img = np.flip(img,axis = 1)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv,red_lower1,red_upper1) + cv2.inRange(hsv,red_lower2,red_upper2)
    # mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,np.ones((9,9),np.uint8))
    mask = cv2.erode(mask,np.ones((7,7),np.uint8))
    mask = cv2.dilate(mask,np.ones((3,3),np.uint8))
    # mask = cv2.erode(mask,np.ones((3,3),np.uint8))
    mask_inv = cv2.bitwise_not(mask)
    bg_masked = cv2.bitwise_and(background,background,mask = mask)
    img_masked = cv2.bitwise_and(img,img,mask = mask_inv)
    output = cv2.addWeighted(bg_masked,1,img_masked,1,0)
    out.write(output)
    cv2.imshow("O/P",output)
    if cv2.waitKey(10) == 27:
        break
cap.release()
out.release()
exit()
