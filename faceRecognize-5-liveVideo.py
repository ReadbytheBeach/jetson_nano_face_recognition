import face_recognition
import cv2
import os
import pickle
import numpy as np
print('cv2 ', cv2.__version__)
print('face_recognition ', face_recognition.__version__)
print('numpy ', np.__version__)

Encodings = []
Names = []

cam=cv2.VideoCapture(0)

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
    frameSmall = cv2.resize(frame,(0,0),fx = .25, fy =.25)
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
        # resize to original frame size, than show the screen
        top, right, bottom, left = top*4, right*4, bottom*4, left*4        
        cv2.rectangle(frame,(left, top),(right,bottom),(0,0,255),2)
        cv2.putText(frame,name,(left,top-6),font,.75,(0,255,255),2)
    cv2.imshow('Picture',frame)
    cv2.moveWindow('Picture',0,0)
    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()