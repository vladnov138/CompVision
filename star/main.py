import numpy as np
from skimage.measure import label
from skimage.morphology import binary_erosion

plus_mask = np.zeros((5, 5))
plus_mask[2, :] = 1
plus_mask[:, 2] = 1
cross_mask = np.zeros((5, 5))
cross_mask[[0, 1, 2, 3, 4], [0, 1, 2, 3, 4]] = 1
cross_mask[[0, 1, 2, 3, 4], [4, 3, 2, 1, 0]] = 1
masks = [plus_mask, cross_mask]

data = np.load("stars.npy")
labelled_data = label(data)
stars_num = 0
for mask in masks:
    res = label(binary_erosion(labelled_data, mask))
    size = len(np.unique(res)) - 1  # Убираем 0 (фон), его не считаем
    if np.all(mask == plus_mask):
        print("Количество звезд в виде плюса: ", size)
        stars_num += size
    else:
        print("Количество звезд в виде креста: ", size)
        stars_num += size
print("Количество звезд: ", stars_num)
