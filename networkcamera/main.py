import cv2
import numpy as np
import zmq


def fupdate(value):
    global flimit
    flimit = value

def supdate(value):
    global slimit
    slimit = value

flimit = 24
slimit = 75
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://192.168.0.105:6556")

cv2.namedWindow("Camera")
# cv2.namedWindow("Debug")
cv2.namedWindow("Mask", cv2.WINDOW_KEEPRATIO)
c = -1
cv2.createTrackbar("F", "Mask", flimit, 255, fupdate)
cv2.createTrackbar("S", "Mask", slimit, 255, supdate)
bg = None
while True:
    buffer = socket.recv()
    c += 1
    arr = np.frombuffer(buffer, np.uint8)
    frame = cv2.imdecode(arr, -1)
    # frame = cv2.imread('1.png')
    key = cv2.waitKey(1)
    if key == ord("s"):
        bg = frame
    # thresh = cv2.adaptiveThreshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
    #                                50,
    #                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                cv2.THRESH_BINARY,
    #                                255,
    #                                10)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = cv2.GaussianBlur(gray, (7, 7), 1)
    thresh = cv2.Canny(mask, flimit, slimit)
    mask = cv2.dilate(thresh, None, iterations=4)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    circles = 0
    squares = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        appr = cv2.approxPolyDP(contour, 0.03 * cv2.arcLength(contour, True), True)
        x2, y2, w2, h2 = cv2.boundingRect(appr)
        area = cv2.contourArea(appr)
        obj_type = "Circle"
        if 0.2 < area / (w2 * h2) < 0.66:
            obj_type = 'Square'
            squares += 1
        else:
            circles += 1
    cv2.putText(frame, f"Figs: {len(contours)}, squares: {squares}, circles: {circles}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    cv2.imshow("Debug", mask)
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(500)
    if key == ord("q"):
        break
