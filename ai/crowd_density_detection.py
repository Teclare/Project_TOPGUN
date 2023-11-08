import cv2


#read image
image = cv2.imread('/home/yang/captured_image.jpg')

if image is None:
    print('could not open image')
    
else:
    face_cascade = cv2.CascadeClassifier('/home/yang/haarcascade_frontalface_default.xml')
    
    if face_cascade.empty():
        print('fail to detect face')
        
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        if len(faces) > 5:
            print("Warning: More than 5 people detected!")

#show result
        for(x, y, w, h) in faces:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),2)
    
#show result image
        cv2.imshow('Image', image)

#save result image
        cv2.imwrite('output.jpg', image)

#close all windows
        cv2.waitKey(0)
        cv2.destroyALLWindows()