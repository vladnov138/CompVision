
from time import sleep

import cv2

cv2.namedWindow("Image")

image = cv2.imread('MyImageFromVideo.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 100, 255, 0)[1]
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
flags = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(x, y, w, h)
    # Или это прямоугольник с основным полем, или с полем земли, или формы двери, или формы здания
    if (x == 0 and (y == 0 or w >= 610 and y > 300) or (20 < w <= 40 and 20 < h <= 48) or w > 400 and 20 < h <= 80 or
        150 < w <= 200 and 150 < h <= 302):
        flags.append(True)
    else:
        flags.append(False)
print(flags)
while True:

    cv2.imshow("Image", image)
    key = cv2.waitKey(500)
    if key == ord("q"):
        break
