import cv2
import numpy as np

def getContours(img, cThr=[100,100],showcanny=False,minArea=1000,filter=0,draw=False):
    cv2.namedWindow('contours',cv2.WINDOW_NORMAL)
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgGray,(5,5),1)
    cannyimg = cv2.Canny(imgblur,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgdial = cv2.dilate(cannyimg,kernel=kernel,iterations=3)
    imgthre = cv2.erode(imgdial,kernel,iterations=2)

    cv2.imshow("contours",imgthre)
    cv2.resizeWindow('contours', 500, 500)
    contour,hierarchy = cv2.findContours(imgthre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []
    for j,i in enumerate(contour):
        area = cv2.contourArea(i)
        if area>minArea:
            peri = cv2.arcLength(i,True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            bbox = cv2.boundingRect(approx)
            if filter>0:
                if len(approx) == filter:
                    finalContours.append([len(approx),area,approx,bbox,i])
                else:
                    finalContours.append([len(approx),area,approx,bbox,i])
    finalContours = sorted(finalContours,key=lambda x:x[1] ,reverse=True)
    if draw:
        for con in finalContours:
            cv2.drawContours(img,con[4],-1,(0,0,255),3)
    return img, finalContours
def reorder(mypoints):
    # print(mypoints.shape)
    mypointsnew = np.zeros_like(mypoints)
    mypoints = mypoints.reshape((4,2))
    add = mypoints.sum(1)
    mypointsnew[0] = mypoints[np.argmin(add)]
    mypointsnew[3] = mypoints[np.argmax(add)]
    diff = np.diff(mypoints, axis=1)
    mypointsnew[1] = mypoints[np.argmin(diff)]
    mypointsnew[2] = mypoints[np.argmax(diff)]


    return mypointsnew

def warpImg(img,points,w,h,pad=10):
    # print("These are points we got from biggest:", points,"\n")
    points = reorder(points)
    # print("Those points are now reordered",points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    # print("This is pts1",pts1,"\n","This is pts2",pts2)
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgwarp = cv2.warpPerspective(img,matrix,(w,h))
    imgwarp = imgwarp[pad:imgwarp.shape[0]-pad,pad:imgwarp.shape[1]-pad]

    return imgwarp
def findDist(pts1,pts2):
    return (((pts2[0]-pts1[0])**2 + (pts2[1]-pts1[1])**2)**0.5)