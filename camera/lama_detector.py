import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import sobel, threshold_otsu
from skimage.morphology import label, binary_dilation, binary_closing, binary_opening, binary_erosion
from skimage.measure import regionprops

mask = np.ones((3, 3))

lama = plt.imread("lama_on_moon.png")
# lama = lama[30:-40, 45:-30]
lama = lama.mean(2)
contours = sobel(lama)
thresh = threshold_otsu(contours) * 1.4
contours[contours < thresh] = 0
contours[contours > 0] = 1
labelled = label(binary_dilation(contours))
regions = regionprops(labelled)
max_region = regions[0]
for region in regions:
    if region.area > max_region.area:
        max_region = region
bbox = max_region.bbox
plt.imshow(contours[bbox[0]:bbox[2], bbox[1]:bbox[3]])
plt.colorbar()
plt.show()
