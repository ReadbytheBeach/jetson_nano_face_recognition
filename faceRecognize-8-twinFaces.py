# python Thread not real parallel running -- python use GIL - 'Global in Lock' (CPython only) strategy
from threading import Thread 
import time
import cv2
import numpy as np
import face_recognition
import pickle

print(cv2.__version__)



with open('/home/xj/Desktop/pyPro/faceRecognizer/train.pkl','rb') as f:
    Names = pickle.load(f)
    Encodings = pickle.load(f)


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
            self.frame2 = cv2.resize(self.frame,(self.width,self.height))
    def getFrame(self):
        return self.frame2


# if 2nd camera is Raspi-Camera
# flip = 2
dispW = 640
dispH = 480
# camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

cam1 = vStream(0,dispW,dispH)
cam2 = vStream(1,dispW,dispH)
# cam2 = vStream(camSet)

font = cv2.FONT_HERSHEY_SIMPLEX
startTime = time.time()
dtav = 0 # dt average

scaleFactor = .2
while True:
    try: 
        myFrame1 = cam1.getFrame()
        myFrame2 = cam2.getFrame()
        # print(cam2.getFrame())
        myFrame3 = np.hstack((myFrame1,myFrame2))       

        frameRGB = cv2.cvtColor(myFrame3,cv2.COLOR_BGR2RGB)
        frameRGBsmall = cv2.resize(frameRGB,(0,0),fx=scaleFactor,fy = scaleFactor)
        facePositions = face_recognition.face_locations(frameRGBsmall, model = 'cnn')    
        allEncodings = face_recognition.face_encodings(frameRGBsmall, facePositions)
        for (top,right,bottom,left), face_encoding in zip(facePositions, allEncodings):
            name = 'unkonw person'
            matches = face_recognition.compare_faces(Encodings, face_encoding, tolerance=.38)
            if True in matches:
                first_match_index = matches.index(True)
                name = Names[first_match_index]
                print(name)
            top = int(top/scaleFactor)
            left = int(left/scaleFactor)
            right = int(right/scaleFactor)
            bottom = int(bottom/scaleFactor)
            cv2.rectangel(myFrame3, (left,top),(right,bottom),(0,0,255),-1)
            cv2.putText(myFrame3,name,(left,top-6),font,.75,(0,0,255),2)     
            
        dt = time.time()-startTime
        startTime = time.time()
        dtav = .9*dtav + .1*dt
        fps = 1 / dtav  # maybe we are not grap that fast, but loop such fast, that's why the fps looks so big value
        # print(fps)
        cv2.rectangle(myFrame3,(0,0),(140,40),(0,0,255),-1)
        cv2.putText(myFrame3,str(round(fps,1))+'fps:',(0,25),font, .75, (0,255,255),1)
        cv2.imshow('Combo', myFrame3)
        cv2.moveWindow('Combo',0,0)

    except:
        print('frame not available')

    if cv2.waitKey(1) == ord('q'):
        cam1.capture.release()
        cam2.capture.release()
        cv2.destroyAllWindows()
        exit(1)  # help to get out the thread
        break



