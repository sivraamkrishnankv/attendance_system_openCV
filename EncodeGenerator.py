# this is to collect the makr sand store it as a pickle file

import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


#credentials to connect to db firebase
cred = credentials.Certificate(r"D:\Attendace_system_EE\faceattendancesystem-srk-firebase-adminsdk-eh0jr-0cdc5c2e1f.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-srk-default-rtdb.firebaseio.com/",
    'storageBucket'    :    "faceattendancesystem-srk.appspot.com"
})




# Importing student images
folderPath = 'Images'
pathList = os.listdir(folderPath)
# print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path))) 
    studentIds.append(os.path.splitext(path)[0])  #extracting the name of the files as they are reg nums of the images

#uploading the images to database
    print("image pushing to db")
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    print("Image pushed succesfully.....")
# finding the face encodings
def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #changin color as opencv always runs in bgr while face_recognition uses rgb
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList) #finding encoding for images
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")
# print(encodeListKnown)
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")