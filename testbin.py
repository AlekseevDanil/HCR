import cv2
import numpy as np
from tqdm import tqdm

image = cv2.imread("DetectingWordsNN/data/bin_input/IMG_8036.jpg", 0)
h = image.shape[0]
w = image.shape[1]

# однозначно определить порог
a = 145

new_image = np.zeros((h, w), np.uint8)
for i in tqdm(range(h)):
    for j in range(w):
        if image[i, j] > a:

            new_image[i, j] = 255
        else:
            new_image[i, j] = 0

cv2.imshow("new", new_image)
cv2.waitKey()
