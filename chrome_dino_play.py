#import required libraries
import pyautogui
import cv2
import numpy as np
import time
import pyautogui as pg

time.sleep(5)
#Variables
roi =[0,0,0,0]
dragonpos =0
center_pre = 0
time_pre = time.time()
center_cur = 0
time_cur = time.time()
hit_time =0
font = cv2.FONT_HERSHEY_SIMPLEX


# Crop functionality to get ROI of the Dragon canvas area
def onMouse(event, x, y, flags, param):
    # print(img[x,y])
    global roi
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        roi[0:2] = [x,y]
    if event ==cv2.EVENT_LBUTTONUP:
        print(x,y)
        roi[2:4]=[x,y]
        print(roi)

# Crop functionality to get ROI of the Dragon canvas area 
jumptrigger =False
def onMoused(event, x, y, flags, param):
    global dragonpos
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x,y)
        dragonpos =x
        print("Dragon position",dragonpos)


scrn = pyautogui.screenshot()
img = np.array(scrn)
while 1:
    cv2.imshow('iwin',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.setMouseCallback('iwin', onMouse)
    if((roi[0]> 0) and (roi[2]>0)):
        print(roi)
        roi[3] = roi[3]-roi[1]
        # roi = [0,0,0,0]
        break;

# Infinite loop to play the game
while 1:
    cv2.setMouseCallback('dwin',onMoused)
    scrn = pyautogui.screenshot(region= roi)
    img = np.array(scrn)

    #Process the trees
    imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, imgthresh =  cv2.threshold(imggray, 127, 255, 1)
    im2, contours, hierarchy = cv2.findContours(imgthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow("Image thresh", imgthresh)
    center_cur =1080
    time_cur = time.time()
    for c in contours:
        if len(c)>3:
            cv2.drawContours(img,[c],0,(0,255,2),3)
            x, y, w, h = cv2.boundingRect(c)
            center = int(((2*x)+w)/2)

            if(center > (dragonpos)):
                tempcenter = center
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 2, 255), 2)
                if(center_cur > tempcenter):
                    center_cur = tempcenter

    cv2.circle(img,(center_cur,20),10,(0,0,0),5)

    if((center_cur-dragonpos)<80):
        #pg.press('up')
        pg.keyDown('up')
        pg.keyUp('up')
        #print("Jump")
    cv2.imshow('dwin', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break