import cv2
import numpy as np
from skimage.measure import label, regionprops

image = cv2.imread('balls_and_rects.png')
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

binary = hsv.mean(2) > 0
labelled = label(binary)
regions = regionprops(labelled)

balls_colors = {}
rects_colors = {}
rects = 0
balls = 0
for region in regions:
    color = hsv[region.bbox[0]:region.bbox[2], region.bbox[1]:region.bbox[3], 0]
    # Проверка цвета угла
    key = np.max(color[0])
    if np.all(color[0][0] != 0):
        rects += 1
        rects_colors[key] = rects_colors.get(key, 0) + 1
    else:
        balls += 1
        balls_colors[key] = balls_colors.get(key, 0) + 1

print(f"Всего фигур: {rects + balls}")
print(f"Всего цветов: {len(np.unique(list(rects_colors) + list(balls_colors)))}")
print("#=====================================================#")
print(f"Прямоугольников: {rects}")
print(f"Оттенки прямоугольника: {len(rects_colors)}")
print(rects_colors)
print("#=====================================================#")
print(f"Шаров: {balls}")
print(f"Оттенки шаров: {len(balls_colors)}")
print(balls_colors)
