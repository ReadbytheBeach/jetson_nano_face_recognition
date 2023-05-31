# python Thread not real parallel running -- python use GIL - 'Global in Lock' (CPython only) strategy
from threading import Thread 
import time
import cv2
import numpy as np
print(cv2.__version__)

startTime = time.time()
font = cv2.FONT_HERSHEY_SIMPLEX
dtav = 0 # dt average

class vStream:
    # resize camera
    # launch camera
    # capture frame
    # show frame
    def __init__(self,src,width,height):
        self.width = width
        self.height = height
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target = self.update, args=())
        self.thread.daemon = True  # when kill the program also kill the thread
        self.thread.start()
    def update(self):
        while True:
            _,self.frame = self.capture.read()
            self.frame = cv2.resize(self.frame,(self.width,self.height))
    def getFrame(self):
        return self.frame



# if 2nd camera is Raspi-Camera
# flip = 2
dispW = 640
dispH = 480
# camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam1 = vStream(0,dispW,dispH)
cam2 = vStream(1,dispW,dispH)
# cam2 = vStream(camSet)

while True:
    try: 
        frameCombined = np.vstack((cam1.getFrame(),cam2.getFrame()))       
        dt = time.time()-startTime
        startTime = time.time()
        dtav = .9*dtav + .1*dt
        fps = 1 / dtav  # maybe we are not grap that fast, but loop such fast, that's why the fps looks so big value
        # print(fps)
        cv2.rectangle(frameCombined,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(frameCombined,'fps:'+str(round(fps,1)),(0,25),font, .75, (0,255,255),1)
        cv2.imshow('ComboCam', frameCombined)
        # myFrame1 = cam1.getFrame()
        # myFrame2 = cam2.getFrame()q
        # cv2.imshow('webCam1', myFrame1)
        # cv2.imshow('webCam2', myFrame2)   
        cv2.moveWindow('ComboCam',0,0)
    except:
        print('frame not available')
    if cv2.waitKey(1) == ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)  # help to get out the thread
        break