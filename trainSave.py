import face_recognition
import cv2
import os
import pickle
print(cv2.__version__)
print(face_recognition.__version__)

Encodings = []
Names = []

image_dir = '/home/xj/Desktop/pyPro/faceRecognizer/demoImages/known'
for root, dirs, files in os.walk(image_dir):
    print(files)
    for file in files:
        path =  os.path.join(root, file)
        print(path)
        # take the picture name
        name = os.path.splitext(file)[0]
        print(name)
        person = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)
print(Names)

# it's a cool app -- pickle in python
# pickle.dump(object, file): put the python data to a pickle format file
with open('train.pkl','wb') as f:
    pickle.dump(Names, f)
    pickle.dump(Encodings, f)
