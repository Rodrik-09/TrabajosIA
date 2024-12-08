import cv2 as cv 
import numpy as np

img = cv.imread('colores.png', 1)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
lower_color = np.array([0, 40, 40])
upper_color = np.array([12, 255, 255])
maskcolor = cv.inRange(hsv, lower_color, upper_color)
    
    # Filtrar la máscara con operaciones morfológicas
mask = cv.erode(maskcolor, None, iterations=2)
mask = cv.dilate(mask, None, iterations=2)

cv.imshow('img', img)
cv.imshow('maskcolor', maskcolor)
cv.imshow('mask', mask)



cv.waitKey(0)
cv.destroyAllWindows()