import cv2 as cv

# Cargar el video
cap = cv.VideoCapture('C:/Users/rbece/Documents/iaP/videos-coches/spark/sparkR9.mp4')
i = 0  

while True:
    ret, frame = cap.read()
    
    # Verificar si el fotograma fue leído correctamente
    if not ret:
        break
    frame_resized = cv.resize(frame, (37, 21), interpolation=cv.INTER_AREA)
    cv.imwrite(f'C:/Users/rbece/Documents/iaP/dataset-coches/Spark/sparkR9-{i}.jpg', frame_resized)
    cv.imshow('Frame', frame_resized)
    i += 1
    
    # Salir con la tecla ESC
    if cv.waitKey(1) == 27:
        break

cap.release()
cv.destroyAllWindows()
