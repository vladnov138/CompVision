import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label
from scipy.ndimage.morphology import binary_opening

files = [file for file in os.listdir("./wires")]
struct = np.ones((3, 1))
for file in files:
    print("File: ", file)
    image = np.load(f"wires/{file}")
    labelled_image = label(image)[0]
    num_wires = np.max(labelled_image)
    for wire_idx in range(1, num_wires + 1):
        wire = np.zeros_like(image)
        wire[labelled_image == wire_idx] = 1
        cut_wire = label(binary_opening(wire, struct))[0]
        num = np.max(cut_wire)
        wire_width = np.sum(wire, axis=1)
        wire_width = len(wire_width[wire_width != 0])
        if wire_width == 2:
            print(f"Провод {wire_idx} разорван в клочья!")
        elif num > 1:
            print(f"Провод {wire_idx} разделен на {num} кусков")
        else:
            print(f"Провод {wire_idx} не поврежден")
    plt.imshow(image)
    plt.show()
    print()
