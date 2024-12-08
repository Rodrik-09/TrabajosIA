import numpy as np
import cv2 as cv
import math 

rostro = cv.CascadeClassifier('haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  
while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
   # _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
    
    # Contar píxeles blancos y negros
   
    
    
    
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    for(x, y, w, h) in rostros:
        frame = cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        
        frame3 = frame[y:y+h, x:x+w]
        frame2 = cv.resize(frame, (100, 100), interpolation=cv.INTER_AREA)
        frame3 = cv.resize(frame, (80, 80), interpolation=cv.INTER_AREA)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame2 = gray[y:y+h, x:x+w]
        _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        white_pixels = np.sum(binary == 255)
        black_pixels = np.sum(binary == 0)
        frame3 = binary[y:y+h, x:x+w]
        print(f'Píxeles blancos: {white_pixels}, Píxeles negros: {black_pixels}')
        cv.imshow('rostror', frame2)
        cv.imshow('rostrors', frame3)
    cv.imshow('rostros', frame)
    i = i+1
    k = cv.waitKey(1)
    if k == 27:
        break
cap.release()
cv.destroyAllWindows()
