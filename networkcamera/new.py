import cv2
import numpy as np

image = cv2.imread("arrow.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 10, 255, 0)[1]

contours = cv2.findContours(thresh, cv2.RETR_TREE,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
print(len(contours))
arrow = contours[0]
print(f"Area = {cv2.contourArea(arrow)}")
print(f"Perimeter = {cv2.arcLength(arrow, False)}")
print(f"Perimeter = {cv2.arcLength(arrow, True)}")

moments = cv2.moments(arrow)
print(moments)

centroid = (int(moments['m10'] / moments['m00']),
            int(moments['m01'] / moments['m00']))
cv2.circle(image, centroid, 5, (0, 255, 0), 4)

eps = 0.001 * cv2.arcLength(arrow, True)
approx = cv2.approxPolyDP(arrow, eps, True)
for p in approx:
    cv2.circle(image, tuple(*p), 6, (0, 255, 0), 2)

hull = cv2.convexHull(arrow)
for i in range(1, len(hull)):
    cv2.line(image, tuple(*hull[i - 1]), tuple(*hull[i]), (0, 255, 0), 2)
cv2.line(image, tuple(*hull[-1]), tuple(*hull[0]), (0, 255, 0), 2)

x, y, w, h = cv2.boundingRect(arrow)
cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

rect = cv2.minAreaRect(arrow)
box = cv2.boxPoints(rect)
box = np.intp(box)
cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

(x, y), rad = cv2.minEnclosingCircle(arrow)
center = int(x), int(y)
rad = int(rad)
cv2.circle(image, center, rad, (0, 255, 0), 2)

ellipse = cv2.fitEllipse(arrow)
cv2.ellipse(image, ellipse, (0, 255, 0), 2)

vx, vy, x, y = cv2.fitLine(arrow, cv2.DIST_L2, 0, 0.01, 0.01)
lefty = int((-x * vy / vx) + y)
righty = int(((image.shape[0] - x) * vy / vx) + y)
cv2.line(image, (image.shape[0] - 1, righty), (0, lefty), (0, 255, 0), 2)

cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)
cv2.waitKey(0)
