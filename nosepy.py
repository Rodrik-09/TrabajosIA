import cv2 as cv
img = cv.imread('tr.jpg',0)
img = cv.cvtColor(img, cv.COLOR_BG2GRAY)
img = cv.cvtColor(img, cv.COLOR_BG2RGB)
img = cv.cvtColor(img, cv.COLOR_BG2HSV)

cv.imshow(img,)