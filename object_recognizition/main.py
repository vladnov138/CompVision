import numpy as np
from skimage.morphology import label, binary_erosion

names = {
    0: "Прямоугольник вырезом влево",
    1: "Прямоугольник вырезом вниз",
    2: "Прямоугольник вырезом вправо",
    3: "Прямоугольник вырезом вверх",
    4: "Просто прямоугольник",
}

data = np.load("ps.npy.txt")
mask = np.zeros((6, 6))
mask[:, 2:] = 1
mask[2:4, 2:4] = 0
rect_mask = np.ones((6, 6))
rect_mask[:2, :] = 0

common_obj_counts = np.max(label(data))
print("Всего фигур: ", common_obj_counts)
obj_counts = {}
# Считаем заранее кол-во прямоугольников, т.к. иначе наша маски и на них срабатывает и у нас потом не сходится
rect_counts = np.max(label(binary_erosion(data, rect_mask)))
obj_counts[names[4]] = rect_counts
for i in range(4):
    count = np.max(label(binary_erosion(data, mask)))  # оставляем только те, что совпали по маске (not max)
    obj_counts[names[i]] = count
    mask = np.rot90(mask)
# Убираем прямоугольники, которые мы посчитали несколько раз для верха и низа
obj_counts[names[1]] -= rect_counts
obj_counts[names[3]] -= rect_counts
print(obj_counts)
