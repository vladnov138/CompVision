import mss
import cv2
import numpy as np
import pyautogui
import time


def process_image(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY, 11, 2)
    return processed_img

def detect_dino(img):
    dino_image = cv2.imread('./assets/1.png', cv2.IMREAD_GRAYSCALE)
    dino_image = cv2.Canny(dino_image, 100, 200)
    screenshot = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    screenshot = cv2.Canny(screenshot, 100, 200)
    w, h = dino_image.shape
    result = cv2.matchTemplate(screenshot, dino_image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc, (max_loc[0] + w, max_loc[1] + h)

def detect_cactus(dino_coords, dino_wh, offset):
    # 80
    # 56, 97 + (offset // 6)
    monitor = {"top": 340, "left": 87,
               "width": 66 + offset, "height": 10}
    screenshot = np.array(sct.grab(monitor))
    # cv2.imshow('Processed', screenshot)
    return np.any(screenshot <= 83)


pyautogui.keyDown('space')
pyautogui.keyUp('space')
with mss.mss() as sct:
    # Поменять при смене экрана
    # monitor = {"top": 220, "left": 300, "width": 600, "height": 150}
    monitor = {"top": 220, "left": 0, "width": 600, "height": 150}
    dino_roi = [100, 350, 200, 400]  # [x_start, y_start, x_end, y_end]
    cactus_roi = [200, 350, 600, 400]  # [x_start, y_start, x_end, y_end]
    prev_y = None
    dino = None
    last_time = time.time()
    lt = last_time
    lim = 20
    offset = 0
    offset_t = 0
    stop = False
    stop2 = False
    stop3 = False
    while True:
        current_time = time.time()
        # lt = current_time
        t_diff = (current_time - last_time)
        # offset_coords = 0
        print(t_diff)
        if t_diff > 30 and not stop2:
            offset_t += 0.02
            offset += 20
            stop2 = True
        if t_diff > 100 and not stop3:
            offset += 50
            offset_t += 0.005
            stop3 = True
        if t_diff > lim and not stop:
            offset += 6
            offset_t += 0.008
            if lim >= 50:
                stop = True
                offset += 17
                lim = 100000000
                offset_t += 0.012
            lim = 50
        screenshot = np.array(sct.grab(monitor))
        binary = process_image(screenshot)
        if dino is None:
            dino = detect_dino(screenshot)
        cactus_coords = detect_cactus(dino[0], dino[1], offset)
        print(dino, cactus_coords)
        prev_y = dino[0][1]
        if (cactus_coords):
            # time.sleep(0.02)
            pyautogui.keyUp('down')
            # time.sleep(0.001)
            pyautogui.keyDown('space')
            pyautogui.keyUp('space')
            time.sleep(0.055 - offset_t)
            pyautogui.keyDown('down')

        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
