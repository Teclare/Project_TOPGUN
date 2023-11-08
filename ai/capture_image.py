import cv2

#connect camera
cap = cv2.VideoCapture(0)

#check camera connect
if not cap.isOpened():
    print('camera connect fail')
    exit()
    
#capture camera frame
ret, frame = cap.read()

#save image if capture success
if ret:
    cv2.imwrite("captured_image.jpg", frame)
else:
    print("image capture fail")
    
#disconnect camera
cap.release()