import cv2
import numpy as np

logo = cv2.imread('../cv2logo/cvlogo.png')
mush = cv2.imread('../cv2logo/mushroom.jpg')
andrey = cv2.imread('andrey.jpg')
rose = cv2.imread('../cv2logo/rose.jpg')
hsv = cv2.cvtColor(rose, cv2.COLOR_BGR2HSV)

lower = np.array([0, 30, 0])
upper = np.array([0, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(rose, rose, mask=mask)

# logo = cv2.resize(logo, (logo.shape[1] // 2, logo.shape[0] // 2))
# andrey = cv2.resize(andrey, (andrey.shape[1] // 2, andrey.shape[0] // 2))
#
# logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
# andrey_gray = cv2.cvtColor(andrey, cv2.COLOR_BGR2GRAY)
#
# ret, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
# a_ret, a_mask = cv2.threshold(andrey_gray, 80, 50, cv2.THRESH_BINARY)
#
# # Вырезаем
# roi = mush[:logo.shape[0], :logo.shape[1]]
# mask_inv = cv2.bitwise_not(mask)
# bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
# fg = cv2.bitwise_and(logo, logo, mask=mask)
# combined = cv2.add(bg, fg)
# roi = mush[:andrey.shape[0], mush.shape[1] - andrey.shape[1]:]
# mask_inv = cv2.bitwise_not(a_mask)
# bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
# fg = cv2.bitwise_and(andrey, andrey, mask=a_mask)
# combined2 = cv2.add(bg, fg)
#
# mush[:logo.shape[0], :logo.shape[1], :] = combined
# mush[:andrey.shape[0], mush.shape[1] - andrey.shape[1]:, :] = combined2

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
