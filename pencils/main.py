import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

images = sorted(os.listdir('./images'),
                key=lambda name: int(name[name.find('(') + 1:name.find(')')]))
print("Files: ", images)
total = 0
for image in images:
    img = cv2.imread(f"images/{image}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Бинаризируем и убираем шумы
    binary = cv2.adaptiveThreshold(gray,
                                   255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,
                                   255,
                                   17)
    # _, binary = cv2.threshold(gray, 128, 192, cv2.THRESH_OTSU)
    binary = cv2.bitwise_not(binary)  # invert
    kernel = np.ones((15, 15), 'uint8')
    img_dilation = cv2.dilate(binary, kernel, iterations=7)
    img_erode = cv2.erode(img_dilation, kernel,
                          iterations=10)
    # Контуры
    canny = cv2.Canny(img_erode, 0, 255)
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    pencils = 0
    for cont in contours:
        p = cv2.arcLength(cont, True)
        rect = cv2.minAreaRect(cont)
        box = cv2.boxPoints(rect)
        width = np.linalg.norm(np.abs(box[0] - box[2]))
        height = np.linalg.norm(np.abs(box[1] - box[3]))
        length_of_object = max(width, height)
        if 2500 <= length_of_object < 3000:
            pencils += 1
    print(f"Кол-во карандашей в {image}: {pencils}")
    total += pencils
    # Uncomment to show the image
    # plt.imshow(img_erode)
    # plt.show()
print("Всего: ", total)
