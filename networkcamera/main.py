import cv2
import numpy as np
import zmq
from skimage.measure import label


def fupdate(value):
    global flimit
    flimit = value

def supdate(value):
    global slimit
    slimit = value

flimit = 78
slimit = 49
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")
socket.connect("tcp://192.168.0.100:6556")

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
    key = cv2.waitKey(1)
    if key == ord("s"):
        bg = frame
    thresh = cv2.Canny(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), flimit, slimit)
    mask = cv2.GaussianBlur(thresh, None, 12)
    mask = cv2.dilate(mask, None, iterations=5)
    labelled = label(mask)
    cv2.putText(frame, f"{np.max(labelled) - 1}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0))
    cv2.imshow("Debug", mask)
    cv2.imshow("Camera", frame)
    # diff = cv2.absdiff(bg, frame)
    # _, mask = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
    #                                cv2.THRESH_BINARY, 11, 2)
    # val, thresh = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
    #                             0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imshow("Debug", thresh)
    # last_img = frame
    key = cv2.waitKey(500)
    if key == ord("q"):
        break
