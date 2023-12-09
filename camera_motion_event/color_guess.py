import random
import time

import cv2

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
capture.set(cv2.CAP_PROP_EXPOSURE, -5)  # Чем меньше число, тем меньше экспозиция
capture.set(cv2.CAP_PROP_TEMPERATURE, 10)

cv2.namedWindow("Camera")
# cv2.namedWindow("Background")
# cv2.namedWindow("Debug")

# lower_yellow = (18, 80, 100)  # yellow
# upper_yellow = (30, 240, 255)
# lower_blue = (93, 100, 115)  # blue
# upper_blue = (125, 205, 255)
# lower_green = (55, 80, 150)  # green
# upper_green = (80, 160, 185)
# lower = (0, 60, 255)  # red
# upper = (185, 160, 255)
# red = [(150, 120, 100), (180, 190, 130)]
orange = [(0, 110, 210), (10, 240, 230)]
yellow = [(18, 80, 100), (30, 240, 255)]
blue = [(93, 100, 115), (125, 205, 255)]
green = [(55, 80, 150), (80, 160, 185)]
colors = [yellow, blue, green, orange]

last_x = None
last_y = None
t_prev = time.perf_counter()
is_guessed = True


def detect_ball(color):
    coords = None
    mask = cv2.inRange(hsv, color[0], color[1])
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])  # свои номера в моментах
        coords = center
        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    return coords


while capture.isOpened():
    coords = []
    noneFlag = False
    if is_guessed:
        is_guessed = False
        random.shuffle(colors)
        print(colors)
    t_current = time.perf_counter()
    ret, frame = capture.read()
    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    coords.append(detect_ball(colors[0]))
    coords.append(detect_ball(colors[1]))
    coords.append(detect_ball(colors[2]))
    coords.append(detect_ball(colors[3]))
    # print(coords)
    for coord in coords:
        if coord is None:
            noneFlag = True
    if (not noneFlag and abs(coords[0][1] - coords[2][1]) <= 100 and coords[0][0] - coords[1][0] <= 100
            and abs(coords[1][1] - coords[3][1]) <= 100 and coords[1][0] - coords[3][0] <= 100):
        cv2.putText(frame, f"Guessed!!!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
    # for i in range(2):
    #     # print(coords[i], coords[i + 1])
    #     if (coords[i] is None or coords[i + 1] is None
    #             or abs(coords[i + 1][1] - coords[i][1]) > 100
    #             or coords[i + 1][0] - coords[i][0] > 250
    #             or coords[i + 1][0] - coords[i][0] < 0):
    #         # print('break')
    #         break
    #     else:
    #         cv2.putText(frame, f"Guessed!!!", (10, 30),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 127))
    # cv2.imshow("Debug", mask)
    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

capture.release()
cv2.destroyAllWindows()
