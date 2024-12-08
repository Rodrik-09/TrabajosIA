import cv2 as cv

cap= cv.VideoCapture(0)

while(True):
    ret, img=cap.read()
    if ret== True:
        cv.imshow('img', img)
        k=cv.waitKey(1) & 0xFF
    if k==27 :
        break
    else:
        break
cap.release()
cv.destroyAllWindows()
