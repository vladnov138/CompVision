from pathlib import Path

import numpy as np
import os

FOLDER = "figures"
files = [file for file in os.listdir(FOLDER) if file.endswith(".txt")]

for file in files:
    print("file: ", file)
    size = np.loadtxt(Path(FOLDER) / Path(file), max_rows=1)
    d = np.loadtxt(Path(FOLDER) / Path(file), skiprows=1)
    max_sum = max(np.sum(d, axis=1))
    if max_sum != 0:
        print("Номинальное разрешение: ", size / max_sum)
    else:
        print("Изображения нет.")