import cv2

cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cam = cv2.VideoCapture(0)

while cam.isOpened():
    ret, frame = cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2YCrCb)
    cv2.imshow("Camera", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
