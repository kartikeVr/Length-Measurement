import cv2
import numpy as np
import test1

webcam = False
path = r"D:\python_projects\length measurement\length measurement.py\1.jpg"
cam = cv2.VideoCapture(1)
cam.set(10, 160)
cam.set(3, 1980)
cam.set(4, 1080)
scale = 3

wP = 210 * scale
hP = 297 * scale

while True:
    if webcam:
        success, img = cam.read()
    else:
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        img = cv2.imread(path)
        
    img, conts = test1.getContours(img, minArea=50000, filter=4, draw=True)

    if len(conts) != 0:
        biggest = conts[0][2]
        # print(f"Biggest contour points: {biggest}")  # Debug print to see the points
        if len(biggest) == 4:  # Ensure there are exactly 4 points
            imgWarp = test1.warpImg(img, biggest, wP, hP)
            img2, conts2 = test1.getContours(imgWarp, minArea=2000, filter=4, cThr=[50, 50], draw=True)
            
            if len(conts2) != 0:
                for obj in conts2:
                    cv2.polylines(img2, [obj[2]], True, (0, 255, 0), 2)
                    nPoints = test1.reorder(obj[2])
                    wl = round(((test1.findDist([nPoints[0][0][0]//scale,nPoints[0][0][1]//scale], nPoints[1][0] // scale)) // 10), 2)
                    hl = round(((test1.findDist(nPoints[0][0] // scale, nPoints[2][0] // scale)) // 10), 2)
                    cv2.arrowedLine(img2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[0][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                    cv2.arrowedLine(img2, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[0][0][1]), (255, 0, 255), 3, 8, 0, 0.05)
                    x, y, w, h = obj[3]
                    cv2.putText(img2, "{}cm".format(wl), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    cv2.putText(img2, "{}cm".format(hl), (x + 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
                    print("So these are the nPoints[0][0]",nPoints[0][0],"till here\nnPoints[1][0]",nPoints[1][0],"Then here\nnPoints[2][0]",nPoints[2][0])
                    print("\nnpoints=",nPoints[0][0][0])

            cv2.imshow("Object", img2)

    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    kernel = np.ones((5, 5))
    cv2.imshow("image", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
