import socket
import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import regionprops, label


def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def centroid(labelled, label=1):
    pos = np.where(labelled == label)
    return pos[0].mean(), pos[1].mean()


host = "84.237.21.36"
port = 5152

plt.ion()
plt.figure()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    beat = b"nope"
    sock.connect((host, port))
    while beat != b"yep":
        sock.send(b"get")
        bts = recvall(sock, 40002)

        img = np.frombuffer(bts[2:40002], dtype="uint8").reshape(bts[0], bts[1])

        # pos1 = np.unravel_index(np.argmax(img), img.shape)
        bin_img = img
        bin_img[bin_img > 0] = 1
        labelled = label(bin_img)
        pos1 = centroid(labelled, 1)
        pos2 = centroid(labelled, 2)
        res = round(np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2), 1)
        print(res)
        # res = np.abs(np.array(pos1) - np.array(pos2))

        sock.send(f"{res}".encode())
        print(sock.recv(4))

        plt.clf()
        plt.imshow(img)
        plt.pause(3)

        sock.send(b"beat")
        beat = sock.recv(20)
