import face_recognition
import cv2
import os
print(cv2.__version__)
print(face_recognition.__version__)

# add the faces should be recognized
Encodings = []
Names = []

"""
donFace = face_recognition.load_image_file('/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known/Donald Trump.jpg')
# maybe found serveral faces, so create an array, but only select the 1st one -- array[0]
# face_recognition.face_encodings() can recognize several faces in one picture. so if only gave a singal face pic, then the array[0] will just be this person be recognized
donEncode = face_recognition.face_encodings(donFace)[0] 

nancyFace = face_recognition.load_image_file('/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known/Nancy Pelosi.jpg')
# maybe found serveral faces, so create an array, but only select the 1st one -- array[0]
nancyEncode = face_recognition.face_encodings(nancyFace)[0] 

xjFace = face_recognition.load_image_file('/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known/XUN Jie.JPG')
# maybe found serveral faces, so create an array, but only select the 1st one -- array[0]
xjEncode = face_recognition.face_encodings(xjFace)[0] 

jiaweiFace = face_recognition.load_image_file('/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known/Jiawei.JPG')
# maybe found serveral faces, so create an array, but only select the 1st one -- array[0]
jiaweiEncode = face_recognition.face_encodings(jiaweiFace)[0] 


# Encoding list.index(n) with Names list.index(n) should be mapped one by one
Encodings = [donEncode, nancyEncode, xjEncode, jiaweiEncode]
Names = ['The Donald', 'Nance Pelosi','Xun Jie','Zhou Jiawei']
"""

# testing an unkown picture, to recognized the trained-person
font = cv2.FONT_HERSHEY_SIMPLEX
testImage = face_recognition.load_image_file('/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known/XUN Jie.jpg')
# print('testImage: ', testImage)

# face_recognition.face_locations(): located the positions for all the recognized faces
# every face has four position info: (top,right,bottom,left), stored in a tuple(), means face_rectangle up-left position and bottom-right position
facePositions = face_recognition.face_locations(testImage)
print('testImage facePositions: ', facePositions)

# collect the face_code for all the recognized faces. 
# A picture may have several faces, so the face_recognition.face_encoding() returns a list, later could add list.index() for recurse
# every face is a 128-Dimension vector
allEncodings = face_recognition.face_encodings(testImage, facePositions) # this is an array
print('allEncodings[0]= ', allEncodings[0])

# transfer to cv2.BGR format
testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

'''
additional: 
to see the face characteristic dict, following codes as an example
includes all the facial feature to compare, which could be classify by 9-types:  
    facial_features = [
                    'chin',
                    'left_eyebrow',
                    'right_eyebrow',
                    'nose_bridge',
                    'nose_tip',
                    'left_eye',
                    'right_eye',
                    'top_lip',
                    'bottom_lip',
                    ]
'''
face_landmarks_list = face_recognition.face_landmarks(testImage)
for face_landmarks in face_landmarks_list:
    print('face_landmarks: {}'.format(face_landmarks))
    
# identify all the recognized people and show the name 
# facePosition: describe by top, right, bottom, left 
# face_encoding: describe by allEncodings by 128-Dimension vector
print(type(facePositions), type(allEncodings))
# use zip: package the array elements to tuple, also zip() as an iterable output
for (top, right, bottom, left), face_encoding in zip(facePositions,allEncodings):   
    name = 'Unkown Person'
    # face_recognition.compare_faces(para1, para2), para1: a face_code list with all the idetified face, para2: a face want to compare
    # so para2 will compare with para1 by each face_code (128-dimension), and return a Boolean-True/False Array, tolerance default = 0.6, the lower the more restrict.
    matches = face_recognition.compare_faces(Encodings, face_encoding)  # return a boolean array for each face, for example, in this case: return four face_code result
    print('matches result: ', matches)
    if True in matches:
        first_match_index = matches.index(True)
        name = Names[first_match_index]
    cv2.rectangle(testImage,(left,top),(right,bottom),(0,0,255),2)
    cv2.putText(testImage,name,(left-6,top-6),font,0.5,(0,255,255),2)

    # each cycle compare one person in the database
    # break

cv2.imshow('myWindow', testImage)  
cv2.moveWindow('myWindow',0,0)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows() 

