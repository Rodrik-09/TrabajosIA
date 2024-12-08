import numpy as np
import cv2 as cv
import math 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        frame2 = frame[ y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)
        frame3 = cv.resize(frame2, (80, 80), interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        frame3 = cv.resize(binary, (80, 80), interpolation=cv.INTER_AREA)
         #frame3 = frame[x+30:x+w-30, y+30:y+h-30]
        
       # cv.imwrite('pruebacaras/rodri'+str(i)+'.jpg', frame2)
        cv.imshow('rostror', frame2)
        #cv.imshow('rostrors', gray)
        cv.imshow('rostrorss', binary)
        cv.imshow('rostdsegs', frame3)
        w100 = np.sum(binary == 255)
        b100 = np.sum(binary == 0)
        w80 = np.sum(frame3 == 255)
        b80 = np.sum(frame3 == 0)
        print(f'Píxeles blancos 100x100: {w100}, Píxeles negros 100x100: {b100}')
        

        print(f'Píxeles blancos 80x80: {w80}, Píxeles negros 100x100: {b80}')

    cv.imshow('rostros', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()