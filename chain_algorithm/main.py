import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x+1), (y, x-1), (y-1, x), (y+1, x)


def neighbours8(y, x):
     return neighbours4(y, x) + ((y-1, x+1), (y+1, x+1), (y-1, x-1), (y+1, x-1))


def get_boundaries(labelled, label=1, connectivity=neighbours4):
    pos = np.where(labelled == label)
    bounds = []
    for y, x in zip(*pos):
        for yn, xn in connectivity(y, x):
            if yn < 0 or yn > labelled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif xn < 0 or xn > labelled.shape[0] - 1:
                bounds.append((y, x))
                break
            elif labelled[yn, xn] == 0:
                bounds.append((y, x))
                break
    return bounds


def get_chain(labelled, label=1, connectivity=neighbours4):
    # Это костыль для маркировки углов, чтобы значения совпали с выданной схемой. Как мне сказали,
    # мы в дальнейшем будем с этим работать и желательно чтобы значения совпадали, чтобы могли проверить без проблем
    # работу. Поэтому при необходимости можно раскомментировать и заменить значения на такие, чтобы совпадали.
    # values = {
    #     0: 0,
    #     3: 6,
    #     5: 7,
    #     1: 4,
    #     2: 2,
    #     6: 3,
    #     7: 5,
    #     4: 1,
    # }
    bounds = get_boundaries(labelled, label=label, connectivity=connectivity)
    chain = []
    bounds.append(bounds[0])  # Это чтобы в конце мы вернулись на ту же позицию
    y_start, x_start = bounds[0]
    y, x = bounds[0]
    started = True  # еще один костыль для цикла do..while, которого в питоне нет
    while y != y_start or x != x_start or started:
        started = False
        bounds.remove((y, x))  # Удаляем текущий элемент, чтобы не вернуться назад. Только вперед
        # ВАЖНО! Проверить сначала по основным 4 соседям: Вверх, вниз, вправо, влево. Иначе он может угол пропустить в
        # пользу других соседей, изолировать этот угол, вернуться к нему и его замкнет, и будет в углу сидеть.
        possible_bounds = neighbours8(y, x)
        for possible_bound in possible_bounds:
            if possible_bound in bounds:
                # chain.append(values[possible_bounds.index(possible_bound)])
                chain.append(possible_bounds.index(possible_bound))
                y, x = possible_bound
                break
    return chain


data = np.load("similar.npy")
labelled_data = label(data)
for i in range(1, np.max(labelled_data) + 1):
    print(f"Фигура №{i}: {get_chain(labelled_data, label=i)}")
plt.imshow(data)
plt.show()
