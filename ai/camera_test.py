import cv2

#connecting camera

cap = cv2.VideoCapture(0)

while True:
    #frame capture
    ret, frame = cap.read()
    
    if not ret:
        print("fail to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Frame',gray)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyALLWindeow()