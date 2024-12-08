import numpy as np
import cv2 as cv
import math 

rostro = cv.CascadeClassifier('C:/Users/rbece/Documents/iaP/cars.xml')
cap = cv.VideoCapture('C:/Users/rbece/Documents/iaP/video2.mp4')
i = 0  
while True:
    ret, frame2 = cap.read()
    gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
       #frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
       frame2 = frame2[ y:y+h, x:x+w]
       #frame3 = frame[x+30:x+w-30, y+30:y+h-30]
       frame2 = cv.resize(frame2, (37, 21), interpolation=cv.INTER_AREA)
       cv.imwrite('C:/Users/rbece/Documents/iaP/pruebacaras/rodri'+str(i)+'.jpg', frame2)
       cv.imshow('rostror', frame2)
    cv.imshow('rostros', frame2)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()