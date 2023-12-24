import cv2


def check_image(x, y, w, h):
    return (x == 0 and (y == 0 or w >= 610 and y > 300) or (20 < w <= 40 and 20 < h <= 48) or w > 400 and 20 < h <= 80
            or 150 < w <= 200 and 150 < h <= 302)


image = cv2.imread('Novikov.png')
video = cv2.VideoCapture('output.avi')

image_counter = 0
frame_counter = 0
while True:
    ret, frame = video.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 100, 255, 0)[1]
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    flags = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        flags.append(check_image(x, y, w, h))
    if len(flags) == 5 and all(flags):
        image_counter += 1
    frame_counter += 1
video.release()
print("Кадров с моим рисунком: ", image_counter)
print("Всего кадров: ", frame_counter)
