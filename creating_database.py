# create a database class for emojinator
# author:- Rudra Narayan Mishra

import cv2
import numpy as np
import os

image_x, image_y = 50, 50


def folderCreation(name):
    if not os.path.exists(name):
        os.mkdir(name)
        
def imagesStorage(gid):
    pics = 1200
    cap = cv2.VideoCapture(0)
    x, y, w, h = 300, 50, 350, 350
    
    folderCreation("gestures/"+str(gid))
    pic_no = 0
    flag_sc = False
    frames = 0
    
    while(True):
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask2 = cv2.inRange(hsv, np.array([0, 58, 50]), np.array([30, 255, 255]))
        res = cv2.bitwise_and(frame, frame, mask=mask2)
        gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        median = cv2.GaussianBlur(gray, (5, 5), 0)
        
        kernel_square = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(median, kernel_square, iterations=2)
        opening=cv2.morphologyEx(dilation,cv2.MORPH_CLOSE,kernel_square)
        
        ret, thresh = cv2.threshold(opening, 30, 255, cv2.THRESH_BINARY)
        thresh = thresh[y:y + h, x:x + w]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[1]
        
        if len(contours) > 0:
            contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(contour) > 10000 and frames > 50:
                x1, y1, w1, h1 = cv2.boundingRect(contour)
                pic_no += 1
                save_img = thresh[y1:y1 + h1, x1:x1 + w1]
                if w1 > h1:
                    save_img = cv2.copyMakeBorder(save_img, int((w1 - h1) / 2), int((w1 - h1) / 2), 0, 0,
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                elif h1 > w1:
                    save_img = cv2.copyMakeBorder(save_img, 0, 0, int((h1 - w1) / 2), int((h1 - w1) / 2),
                                                  cv2.BORDER_CONSTANT, (0, 0, 0))
                save_img = cv2.resize(save_img, (image_x, image_y))
                cv2.putText(frame, "Capturing...", (30, 60), cv2.FONT_HERSHEY_TRIPLEX, 2, (127, 255, 255))
                cv2.imwrite("gestures/" + str(gid) + "/" + str(pic_no) + ".jpg", save_img)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, str(pic_no), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (127, 127, 255))
        cv2.imshow("Capturing gesture", frame)
        cv2.imshow("thresh", thresh)
        keypress = cv2.waitKey(1)
        if keypress == ord('c'):
            if flag_sc == False:
                flag_sc = True
            else:
                flag_sc = False
                frames = 0
        if flag_sc == True:
            frames += 1
        if pic_no == pics:
            break
        
gid = input("Enter gesture number: ")
imagesStorage(gid)