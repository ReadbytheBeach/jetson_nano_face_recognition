import face_recognition
import cv2
import os
import pickle
import numpy as np
import time
print('cv2 ', cv2.__version__)
print('face_recognition ', face_recognition.__version__)
print('numpy ', np.__version__)

# frame per seconds
fpsReport = 0
# scale less, can see more far away face, due to provide more pixels to the algorithm
# but scale less also will accelerate slow, due to provide more pixels to the processors
scaleFactor = .25 

Encodings = []
Names = []

cam=cv2.VideoCapture(0)

timeStamp = time.time()
with open('/home/xj/Desktop/pyPro/faceRecognizer/train.pkl','rb') as f:
    # !!!MUST: load parameters sequence follow the dump parameter sequence!! 
    # for example pickle.dump() sequence is Names, then Encodings, so pickle.load() sequence must be Names first, then Encodings. 
    # So suggest by use print() to check the pickle.load() 
    Names = pickle.load(f)
    # print('Names: ', Names)
    Encodings = pickle.load(f)
    # print('Encodings: ', Encodings)
    # print('Encodings type: ', Encodings[0].dtype)
        
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
    _, frame =  cam.read()
    # make the frame smaller, than will acclerate the processing speed
    # due to resize the frame, please make sure, at the program beginning, try to close to the camera
    frameSmall = cv2.resize(frame,(0,0),fx = scaleFactor, fy =scaleFactor)
    frameRGB = cv2.cvtColor(frameSmall,cv2.COLOR_BGR2RGB)
    # jetson nano could use mode='cnn'
    facePositions = face_recognition.face_locations(frameRGB, model='cnn')
    allEncodings = face_recognition.face_encodings(frameRGB, facePositions)
    # check element type of allEncodings whether is data-type 'float64'
    # print('allEncodings type: ', allEncodings[0].dtype)
      
    # look all the faces(facePositions provided) in the Frame(frameRGB)
    for (top, right, bottom, left),face_encoding in zip(facePositions, allEncodings):
        name = 'Unknow Person'
        # Asia faces not easy for separately, so should reduce the tolerance to 0.35~0.4 
        matches = face_recognition.compare_faces(Encodings, face_encoding, tolerance=0.38)
        if True in matches:
            first_match_index = matches.index(True)
            name = Names[first_match_index]
        # resize to original frame size, then show the screen
        top = int(top/scaleFactor) 
        right = int(right/scaleFactor)
        bottom = int(bottom/scaleFactor)
        left = int(left/scaleFactor)        
        cv2.rectangle(frame,(left, top),(right,bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,255,255),2)
    # measure each frame time duration 
    dt = time.time() - timeStamp
    # measure frames per second
    fps = 1/dt
    fpsReport = .9*fpsReport + .1*fps  # to remove the Noise, so fpsReport = 90% trust the former fpsReport + 10% trust the current fpsReport
    # print('FPS is: ',round(fpsReport,1))
    # show the fps on screen
    cv2.rectangle(frame,(0,0),(100,40),(0,0,255),-1)
    cv2.putText(frame,str(round(fpsReport,1))+'fps',(5,25),font,.75,(0,255,255),1)
    # reset for next cycle calculate from zero
    timeStamp = time.time()
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',0,0)
    if cv2.waitKey(1) == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()