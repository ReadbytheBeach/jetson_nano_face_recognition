import cv2
import numpy as np
import time
print(cv2.__version__)

dispW=640
dispH=480
flip=0  # change camera play direction
# Uncomment These next Two Line for Pi Camera
# camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam= cv2.VideoCapture(0)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
cam_1 =cv2.VideoCapture(0)
cam_2 = cv2.VideoCapture(1)

print(type(cam_1))

font = cv2.FONT_HERSHEY_SIMPLEX
# dt average change
dtav=0

startTime = time.time()
while True:
    ret, frame_1 = cam_1.read()

    ret, frame_2 = cam_2.read()

    # print the frame shape for checking
    print(frame_1.shape)
    # put diff frames into a frame, so need resize the frame, but not consider the diff camera frame may has diff frequency
    # frame(x,y) means opencv(column, row)
    frame_2 = cv2.resize(frame_2, (frame_1.shape[1], frame_1.shape[0]))
    frameCombined = np.hstack((frame_1,frame_2))
    dt = time.time() - startTime
    startTime = time.time()
    dtav = .9*dtav + .1*dt
    fps = 1/dtav 
    cv2.rectangle(frameCombined,(0,0),(130,40),(0,0,255),-1)
    cv2.putText(frameCombined,str(round(fps,1))+'FPS',(2,25),font,.75,(0,255,255),2)
    
    # cv2.imshow('webCam_1',frame_1)
    # cv2.imshow('webCam_2',frame_2)
    cv2.imshow('Combo', frameCombined)

    # cv2.moveWindow('webCam_1',0,0)
    # cv2.moveWindow('webCam_2',700,0)
    cv2.moveWindow('Combo',0,0)
     
    if cv2.waitKey(1)==ord('q'):
        break
        
cam_1.release()
cam_2.release()
cv2.destroyAllWindows()