import cv2
import numpy as np


def blur(arr, size=(10, 10)):
    out = np.zeros_like(arr)
    stepy = out.shape[0] // size[0]
    stepx = out.shape[1] // size[1]
    for y in range(0, arr.shape[0], stepy):
        for x in range(0, arr.shape[1], stepx):
            out[y: y+stepy, x: x+stepy] = np.average(arr[y:y+stepy, x:x+stepy])
    return out


cam = cv2.VideoCapture(0)
cv2.namedWindow("Camera", cv2.WINDOW_KEEPRATIO)
cascade = cv2.CascadeClassifier("haarcascade_eye_tree_eyeglasses.xml")
glasses = cv2.imread('deal_with_it.png')
_, glasses = cv2.threshold(glasses, 50, 255, cv2.THRESH_BINARY)

while cam.isOpened():
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) == 2:
        eye1 = faces[0]
        eye2 = faces[1]
        center1 = eye1[0] + eye1[2] // 2, eye1[1] + eye1[3] // 2
        center2 = eye2[0] + eye2[2] // 2, eye2[1] + eye2[3] // 2
        x1 = min(center1[0], center2[0])
        y1 = min(center1[1], center2[1])
        x2 = max(center1[0], center2[0])
        y2 = max(center1[0], center2[0])
        w = max(center1[0], center2[0]) - x1
        h = max(center1[-1], center2[-1]) - y1
        roi = frame[y1 - h - 50:y2, x1 - w // 2:x1+int(w*1.5)]
        mask = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)
        mask[:, :, :] = 255
        glasses = cv2.resize(glasses, (roi.shape[1], roi.shape[0]))
        mask[y1 - h - 50:y2, x1 - w // 2:x1+int(w*1.5)] = glasses
        indices = np.where(mask[:, :, 0] >= 230)
        mask[indices] = frame[indices]
        frame = mask
    # for (x, y, w, h) in faces:
    #     # cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #     w = int(w * 1.2)
    #     h = int(h * 1.5)
    #     x -= int((w * 1.2 - w) // 2)
    #     y -= int((h * 1.5 - h) // 2)
    #     roi = frame[y:y+h, x:x+w]
    #     blurred = blur(roi, (15, 15))
    #     frame[y:y+h, x:x+w] = blurred
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
