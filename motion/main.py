import os

import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label, regionprops

files = sorted(os.listdir('./out'),
               key=lambda name: int(name[name.find('_') + 1:name.find('.')]))
coords = []
for file in files:
    data = np.load(f'./out/{file}')
    labelled = label(data)
    regions = regionprops(labelled)
    sorted_regions = sorted(regions, key=lambda region: region.area)
    coords.append(sorted_regions[0].centroid)
    coords.append(sorted_regions[1].centroid)
    coords.append(sorted_regions[2].centroid)
np_coords = np.array(coords)
plt.plot(np_coords[::3, 0], np_coords[::3, 1], label='1st ball')
plt.plot(np_coords[1::3, 0], np_coords[1::3, 1], label='2nd ball')
plt.plot(np_coords[2::3, 0], np_coords[2::3, 1], label='3rd ball')
plt.legend()
plt.show()
