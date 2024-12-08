import cv2 as cv
import numpy as np
img = cv.imread('tr.jpg',0)
x, y=img.shape
img2 =np.zeros((x*2,y*2), dtype='uint8')
for i in range(x):
    for j in range(y):
        img2[i*2, j*2]=img[i,j]

print(img.shape)
cv.imshow('img2', img2)
cv.imshow('img', img)
cv.waitKey(0)
cv.destroyAllWindows()


