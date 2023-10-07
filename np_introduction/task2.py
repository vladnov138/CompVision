import numpy as np

img1 = np.loadtxt("./imgs/img1.txt", skiprows=2)
img2 = np.loadtxt("./imgs/img2.txt", skiprows=2)
sum_line1 = np.sum(img1, axis=1)
sum_line2 = np.sum(img2, axis=1)
y1 = np.where(sum_line1 == (sum_line1[sum_line1 != 0])[0])[0][0]  # Find first non-zero element by axis 1
y2 = np.where(sum_line2 == (sum_line2[sum_line2 != 0])[0])[0][0]  # from start of the array
sum_col1 = np.sum(img1, axis=0)
sum_col2 = np.sum(img2, axis=0)
x1 = np.where(sum_col1 == (sum_col1[sum_col1 != 0])[0])[0][0]  # Find first non-zero element by axis 0
x2 = np.where(sum_col2 == (sum_col2[sum_col2 != 0])[0])[0][0]  # from start of the array
print(f"Смещение х: {x2 - x1}, смещение у: {y2 - y1}")
