import cv2
import numpy as np

scale = 3
wP = 200 * scale
hP = 287 * scale

def getContours(img, cThr=[100, 100], showcanny=False, minArea=1000, filter=0, draw=False):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgblur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    cannyimg = cv2.Canny(imgblur, cThr[0], cThr[1])
    if showcanny:
        cv2.imshow("canny", cannyimg)
    kernel = np.ones((5, 5))
    imgdial = cv2.dilate(cannyimg, kernel=kernel, iterations=3)
    imgthre = cv2.erode(imgdial, kernel, iterations=2)

    contour, hierarchy = cv2.findContours(imgthre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalContours = []

    for j, i in enumerate(contour):
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])
    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)
    if draw:
        for con in finalContours:
            cv2.drawContours(img, contour, -1, (0, 0, 255), 3)
    return img, finalContours


def reorder_points(pts):
    if len(pts) > 4:
        peri = cv2.arcLength(pts, True)
        approx = cv2.approxPolyDP(pts, 0.02 * peri, True)
        if len(approx) == 4:
            pts = approx
        else:
            return None
    if len(pts) != 4:
        raise ValueError(f"Expected 4 points to reorder, got {len(pts)}. Points: {pts}")

    pts = pts[np.argsort(pts[:, 0]), :]
    left_most = pts[:2, :]
    right_most = pts[2:, :]

    left_most = left_most[np.argsort(left_most[:, 1]), :]
    top_left, bottom_left = left_most

    right_most = right_most[np.argsort(right_most[:, 1]), :]
    top_right, bottom_right = right_most

    return np.array([top_left, top_right, bottom_left, bottom_right], dtype='float32')


def warp_image(img, points, w, h, pad=10):
    points = reorder_points(points)
    if points is None:
        return img
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped = cv2.warpPerspective(img, matrix, (w, h))
    warped = warped[pad:warped.shape[0] - pad, pad:warped.shape[1] - pad]
    return warped

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    frame = cv2.resize(frame, (900, 500))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)
    edges = cv2.Canny(blurred, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(edges, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        largest_contour = contours[0]
        peri = cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)

        points = approx.reshape(len(approx), 2)

        warped = warp_image(frame, points, hP, wP)

        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 1)
        edges = cv2.Canny(blurred, 100, 100)
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(edges, kernel, iterations=3)
        imgThr = cv2.erode(imgDial, kernel, iterations=2)

        contours, _ = cv2.findContours(imgThr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        img2, conts2 = getContours(warped, minArea=2000, showcanny=True, filter=0, cThr=[50, 50], draw=False)

        for obj in conts2:
            rect = cv2.minAreaRect(obj[4])
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            x, y, w, h = obj[3]
            cv2.drawContours(img2, [box], 0, (0, 255, 0), 2)

            (width, height) = rect[1]
            width_cm = round(width / scale / 10, 1)
            height_cm = round(height / scale / 10, 1)

            cv2.putText(img2, f"W: {width_cm}cm", (int(rect[0][0] - 50), int(rect[0][1] - 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            cv2.putText(img2, f"H: {height_cm}cm", (int(rect[0][0] - 50), int(rect[0][1] + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            ymin, xmin, ymax, xmax = obj[3]
            xmin, xmax, ymin, ymax = (xmin * width, xmax * width, ymin * height, ymax * height)
            xmin, xmax, ymin, ymax = int(xmin), int(xmax), int(ymin), int(ymax)

            cv2.rectangle(img2, (xmin, ymin), (xmax, ymax), color=(0, 210, 0), thickness=1)
            cv2.putText(img2, f"W: {width_cm}cm \n H: {height_cm}cm ", (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1,
                        (0, 210, 0), 2)

            lineWidth = min(int((xmax - xmin) * 0.2), int((ymax - ymin) * 0.2))
            cv2.line(img2, (xmin, ymin), (xmin + lineWidth, ymin), (0, 210, 0), thickness=5)
            cv2.line(img2, (xmin, ymin), (xmin, ymin + lineWidth), (0, 210, 0), thickness=5)

            cv2.line(img2, (xmax, ymin), (xmax - lineWidth, ymin), (0, 210, 0), thickness=5)
            cv2.line(img2, (xmax, ymin), (xmax, ymin + lineWidth), (0, 210, 0), thickness=5)

        cv2.imshow("Detected Shapes", img2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
