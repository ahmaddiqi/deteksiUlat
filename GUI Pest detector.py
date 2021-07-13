#!/usr/bin/env python
import PySimpleGUI as sg #library GUI
#installnya dengan cara pip install PySimpleGUI

import cv2
import numpy as np
import time

#atur tuning disini
scaleValue = 30
neig = 5
minArea = 3520


def main():

    sg.theme('Material1') #warna background program

    path = 'cascade.xml'  #folder dan penamaan file xml harus sesuai dengan path

    objectName = 'Plutella xylostella'  #penamaan object di display/monitor
    frameWidth = 420 #display width
    frameHeight = 210  #display height

    # Capture from the default deivce
    cap = cv2.VideoCapture(0)
    cap.set(3,frameWidth) # set Width
    cap.set(4,frameHeight) # set Height
    color = (255,0,255)
    time.sleep(1)

    def empty(a):
        pass

    
    stringDeteksi = ''
    #desain tampilan dan buat tombol juga
    layout = [[sg.Text('Pendeteksi Plutella Xylostella', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Text(key='jumlahDeteksi', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Button('Mulai', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Keluar', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Pendeteksi Plutella Xylostella',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    #cap = cv2.VideoCapture(0)
    recording = False
    
    while True:
        
        event, values = window.read(timeout=20)
        if event == 'Keluar' or event == sg.WIN_CLOSED:
            exit()
            return

        elif event == 'Mulai':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

            #kalau recording bernilai true dia langsung buka camera
        if recording:
            count = 0
            ret, img = cap.read()
            height,width = img.shape[0:2]
            # cv2.putText(img,'Total Detection Count:',(10,30), cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,255),2)
        
            #download classifiers class
            plutella_cascade = cv2.CascadeClassifier(path)

            #get camera image and convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            #detect objek dengan cascade
            #scale : lower computing lebih besar dan hasil lebih bagus
            scaleVal = 1 + (scaleValue / 1000)
            #lower minimum neighbor akan mendapati banyak objek yang dideteksi, menyebabkan kesalahan deteksi 
            
            
            #objects = cascade.detectMultiScale(gray, scaleVal, neig)    #program convert gambar yang di capture
            objects = plutella_cascade.detectMultiScale(gray, scaleVal, neig)
            for (x, y, w, h) in objects :
                area = w * h
                font = cv2.FONT_HERSHEY_COMPLEX_SMALL
                if area > minArea :
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 191), 3) #bounding box
                    cv2.putText(img, objectName, (x, y - 5), font, 1, color, 2)
                    roi_gray = gray [y:y + h, x:x + w]
                    roi_color = img [y:y + h, x:x + w]
                    count+=1
                plutellacy = int(y+h/2)
                linecy = height-240
                # if ((plutellacy < linecy+6) and (plutellacy > linecy-6)):
                    # count = count+1
                # cv2.putText(img,str(count),(400,30), font,0.8,(255,255,255),2)
                # roi_color = img[y:y + h, x:x + w]

            # display the image on screen and wait for a keypress
            # cv2.imshow("Result", img)
            # key = cv2.waitKey(30) & 0xff
            # if key == 27:
            #     break
            stringDeteksi = "Jumlah terdeteksi : " + str(count) #menampilkan jumlah deteksi di window
            window['jumlahDeteksi'].update(stringDeteksi) #mengupdate nilai deteksi di windows
            imgbytes = cv2.imencode('.png', img)[1].tobytes() #menampilkan image camera di window
            window['image'].update(data=imgbytes) #mengupdate image camera di window
        # cap.release()
        # cv2.destroyAllWindows()

main()