from matplotlib import pyplot as plt
from skimage.measure import regionprops, label
from skimage.morphology import binary_closing


def filling_factor(region):
    return region.image.mean()


def recognize(region):
    if filling_factor(region) == 1:
        return "-"
    euler = region.euler_number
    match euler:
        case -1:  # B | 8
            if region.image.mean(0)[0] == 1:
                return "B"
            return "8"
        case 0:  # A | P | D | 0 | *
            if region.image.mean(0)[0] == 1:  # P or D
                tmp = region.image.copy()
                tmp[tmp.shape[0] // 2, :] = 1
                tmp_regions = regionprops(label(tmp))
                if tmp_regions[0].euler_number == -1:
                    return "D"
                return "P"
            tmp = region.image.copy()
            tmp[-1, :] = 1
            tmp_regions = regionprops(label(tmp))
            if tmp_regions[0].euler_number == -1:  # A or *
                # По идее дефолтной маски хватит, чтобы дырку убрать
                if regionprops(label(binary_closing(tmp)))[0].euler_number == 1:
                    return "*"
                return "A"
            return "0"
        case 1:  # 1 | W | X | / | *
            mean_arr = region.image.mean(0)
            if mean_arr[mean_arr == 1].shape[0] > 1:
                return "1"
            if mean_arr[mean_arr == 1].shape[0] == 1:
                return "*"
            tmp = region.image.copy()
            tmp[-1, :] = 1
            tmp[0, :] = 1
            tmp_regions = regionprops(label(tmp))
            euler = tmp_regions[0].euler_number
            if euler == -1:
                return "X"
            elif euler == -2:
                return "W"
            if region.eccentricity > 0.5:
                return "/"
            return "*"
    return "?"


data = plt.imread("symbols.png")
bin = data.mean(2)
bin[bin > 0] = 1
labelled = label(bin)
count_chars = labelled.max()
print(f"Всего символов: {count_chars}")
regions = regionprops(labelled)
counts = {}
for region in regions:
    symbol = recognize(region)
    if symbol not in counts:
        counts[symbol] = 0
    counts[symbol] += 1
print(counts)
print(f"Процент определения символов: {(count_chars - counts.get('?', 0)) / count_chars * 100}")
plt.imshow(labelled)
plt.show()
