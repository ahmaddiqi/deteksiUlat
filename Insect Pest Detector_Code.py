# import the necessary packages
import cv2
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import numpy as np
import time

# initialize the camera and grab a reference to the raw camera capture
path = 'cascade.xml'  #folder dan penamaan file xml harus sesuai dengan path
#path = '/home/pi/Desktop/Plutella xylostella L/cascade_plutella.xml'
objectName = 'Plutella xylostella'  #penamaan object di display/monitor
frameWidth = 640  #display width
frameHeight = 480  #display height
#color = (255, 0, 255)

# Capture from the default deivce
cap = cv2.VideoCapture(0)
cap.set(3,frameWidth) # set Width
cap.set(4,frameHeight) # set Height
color = (255,0,255)
time.sleep(1)

def empty(a):
    pass

#create trackbar untuk parameter objek yang dideteksi
cv2.namedWindow("Result")
cv2.resizeWindow("Result", frameWidth, frameHeight + 100)
cv2.createTrackbar("Scale", "Result", 400, 1000, empty)
cv2.createTrackbar("Neig", "Result", 8, 50, empty)
cv2.createTrackbar("Min Area", "Result", 0, 100000, empty)
cv2.createTrackbar("Brightness", "Result", 180, 255, empty)

# grab an image from the camera
#camera = PiCamera()
#camera.resolution = (frameWidth, frameHeight)
#camera.framerate = 32

#rawCapture = PiRGBArray(camera, size=(frameWidth, frameHeight))

#download classifiers class
#cascade = cv2.CascadeClassifier(path)

count = 0

#for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
while True:
    # Caputure a single frame
    ret, img = cap.read()
    #img = frame.array
    #set camera brightness from trackbar value
    cameraBrightness = cv2.getTrackbarPos("Brightness", "Result")

    height,width = img.shape[0:2]

    cv2.putText(img,'Total Detection Count:',(10,30), cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)

    #cv2.line(img, (0,height-240),(width,height-240),(0,255,255),2)

    #download classifiers class
    plutella_cascade = cv2.CascadeClassifier(path)

    #get camera image and convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, thresh_gray = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)

    # threshold image
    #ret, threshed_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # find contours and get the external one
    #contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #detect objek dengan cascade
    scaleVal = 1 + (cv2.getTrackbarPos("Scale", "Result") / 1000) #scale : lower computing lebih besar dan hasil lebih bagus
    neig = cv2.getTrackbarPos("Neig", "Result") #lower minimum neighbor akan mendapati banyak objek yang dideteksi, menyebabkan kesalahan deteksi
    #objects = cascade.detectMultiScale(gray, scaleVal, neig)    #program convert gambar yang di capture
    objects = plutella_cascade.detectMultiScale(gray, scaleVal, neig)

    #display objek yang terdeteksi
    for (x, y, w, h) in objects :
        area = w * h
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area > minArea :
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #bounding box
            cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            roi_gray = gray [y:y + h, x:x + w]
            roi_color = img [y:y + h, x:x + w]

        #minArea = cv2.getTrackbarPos("Min Area", "Result")
        #if area > minArea :
            #cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #bounding box
            #cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            #roi_color = img[y:y + h, x:x + w]

        #display count objek yang terdeteksi
    #for (x, y, w, h) in objects:
        plutellacy = int(y+h/2)
            #plutellacy = w * h
        linecy = height-240
        if ((plutellacy < linecy+6) and (plutellacy > linecy-6)):
                #cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #bounding box
                #cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
                #roi_color = img[y:y + h, x:x + w]
            count = count+1 #jumlah object yang terdeteksi
            #cv2.line(img, (0,height-240),(width,height-240),(0,0,255),5)

        #cv2.rectangle(img, (x, y), (x + w, y + h), color, 3) #bounding box
        #cv2.putText(img, objectName, (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
        cv2.putText(img,str(count),(400,30),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
        roi_color = img[y:y + h, x:x + w]

    # display the image on screen and wait for a keypress
    cv2.imshow("Result", img)

    key = cv2.waitKey(30) & 0xff
    #rawCapture.truncate(0)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
