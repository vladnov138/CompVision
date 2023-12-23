import cv2

image = cv2.imread("hierarchy.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 10, 255, 0)[1]

contours, tree = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))
print(tree)

for i, c in enumerate(contours):
    cv2.putText(image, f"{tree[i]}", c[0], cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                (0, 255, 0), 2)


cv2.namedWindow("Image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("Image", image)
cv2.waitKey(0)
