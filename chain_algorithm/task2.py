import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label


def neighbours4(y, x):
    return (y, x + 1), (y + 1, x), (y, x - 1), (y - 1, x)


def neighbours8(y, x):
    return neighbours4(y, x) + ((y - 1, x + 1), (y + 1, x + 1), (y - 1, x - 1), (y + 1, x - 1))


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
    # Это костыль для маркировки углов, чтобы значения совпали с выданной схемой.
    values = {
        0: 0,
        3: 2,
        5: 7,
        1: 6,
        2: 4,
        6: 3,
        7: 5,
        4: 1,
    }
    bounds = get_boundaries(labelled, label=label, connectivity=connectivity)
    chain = []
    # bounds.append(bounds[0])  # Это чтобы в конце мы вернулись на ту же позицию
    y_start, x_start = bounds[0]
    y, x = bounds[1]
    bounds.append(bounds[1])
    started = True  # еще один костыль для цикла do..while, которого в питоне нет
    while len(bounds) > 0:
        started = False
        bounds.remove((y, x))  # Удаляем текущий элемент, чтобы не вернуться назад. Только вперед
        # ВАЖНО! Проверить сначала по основным 4 соседям: Вверх, вниз, вправо, влево. Иначе он может угол пропустить в
        # пользу других соседей, изолировать этот угол, вернуться к нему и его замкнет, и будет в углу сидеть.
        possible_bounds = neighbours8(y, x)
        for possible_bound in possible_bounds:
            if possible_bound in bounds:
                chain.append(values[possible_bounds.index(possible_bound)])
                # chain.append(possible_bounds.index(possible_bound))
                y, x = possible_bound
                break
    return chain


def curvature(chain):
    result = []
    for i in range(len(chain)):
        if i == len(chain) - 1:
            result.append(chain[i] - chain[0])
        else:
            result.append(chain[i] - chain[i + 1])
    return result


def normalize(chain):
    for i in range(len(chain)):
        chain[i] = chain[i] % 8


def check_images(normal_chain1, normal_chain2) -> bool:
    normal_chain2 = normal_chain2[:]
    for i in range(len(normal_chain1)):
        if normal_chain1 == normal_chain2:
            return True
        normal_chain2 = normal_chain2[1:] + [normal_chain2[0]]
    return False


fig1 = np.zeros((5, 5))
fig1[1:3, 1:-1] = 1
# fig1[1, 1] = 0 # Проверка на не совпадение
fig2 = fig1.T
normal_chains = []
for ch in (fig1, fig2):
    labelled = label(ch)
    chain = get_chain(labelled, 1)
    ch = curvature(chain)
    normalize(ch)
    normal_chains.append(ch)
if check_images(normal_chains[0], normal_chains[1]):
    print("Фигуры совпадают")
else:
    print("Фигуры не совпадают")
