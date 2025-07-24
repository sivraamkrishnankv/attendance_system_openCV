import cv2
import os
import pickle, face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
from datetime import datetime
import logging
import os

logging.basicConfig(filename='mainfe.log', level=logging.DEBUG)
logging.debug('Starting script...')

# Rest of your script



#credentials to connect to db firebase
cred = credentials.Certificate(r"D:\Attendace_system\faceattendancesystem-srk-firebase-adminsdk-eh0jr-0cdc5c2e1f.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-srk-default-rtdb.firebaseio.com/",
    'storageBucket'    :    "faceattendancesystem-srk.appspot.com"
})

bucket = storage.bucket()  #to get img from db
id=-1
imgstudent=[]

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread (r'D:\Attendace_system_EE\Resources\background.png')

# addiing the images for the fe in a list to access it based on our preferences (importing mode images into a list)
folderModepath=r'D:\Attendace_system\Resources\Modes'
modePathList=os.listdir(folderModepath)
imgModeList=[ ]
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModepath,path)))

#loading the encoded file
print('loading encoded file.....')
file=open('EncodeFIle.p','rb')
encodeListKnownWithIds=pickle.load(file)
encodeListKnownWithIds, studentIds = encodeListKnownWithIds
print('encoded file loaded')

modeType=0
counter = 0 #to download the img from db only once for detection

while True:
    #running the webcam and imposing it in the resource bg img
    _ , img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) #scaling down the image for faster processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) #color conversion as face recog lib can work in rgb color scheme only

    faceCurFrame = face_recognition.face_locations(imgS) #analyze facial points in the camera (imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame) #encoding the current frame for comparing the encoded points

    imgBackground[ 162:162+480, 55:+55+640 ] = img #fixing the height and width to the image and imposing it
    imgBackground[ 44:44+633, 808:808+414 ] = imgModeList[modeType]
    # cv2.imshow("webcam",imgBackground)
    if faceCurFrame: #only if a frame is detected
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnownWithIds, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnownWithIds, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)

            matchIndex = np.argmin(faceDis) #taking the in value as output which is the correct idetified image in dataset
            # print("Match Index", matchIndex)
            # print('known face detected')

            if matches[matchIndex]:
                # print("Known Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc 
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #upscaling the images by 1/4 th i.e 0.25x4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=1) #drawing a modern face rectangle
                id = studentIds[matchIndex] #to access the info inn db
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loading",(275, 400))
                    cv2.imshow("Face-attendance",imgBackground)
                    cv2.waitKey(1)
                    counter =1
                    modeType=1
        if counter !=0:
            if counter ==1:
                #getting datat from db as per identified by face recognition
                studentInfo = db.reference(f'Students/{id}').get()
                # print(studentInfo)
                blob = bucket.get_blob(f'Images/{id}.png') #gets the image
                array=np.frombuffer(blob.download_as_string(),np.uint8)
                imgstudent= cv2.imdecode(array,cv2.COLOR_BGR2RGB)


                #update data of attendance
                datetimeobject = datetime.strptime(studentInfo['last_attendance_time'],
                                                "%Y-%m-%d %H:%M:%S"  )
                secondsElapsed= (datetime.now()-datetimeobject).total_seconds()
                print(secondsElapsed)
                if secondsElapsed > 3: #attendace interval in seconds 
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] +=1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime( "%Y-%m-%d %H:%M:%S" ))
                else:
                    modeType = 3
                    counter = 0
                imgBackground[ 44:44+633, 808:808+414 ] = imgModeList[modeType]
            if modeType!=3: #run only if th eattendace is not marked already (modetype 3 is already maeked img)
                # using if loops to confirm the attendance counter is no of frames
                if 10<counter<20:
                    modeType=2
                
                imgBackground[ 44:44+633, 808:808+414 ] = imgModeList[modeType]

                if counter<=10:
                    #displayinf details in the op
                    cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['major']),(1006,550),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(id),(1006,493),
                                cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                    cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    cv2.putText(imgBackground,str(studentInfo['starting_year']),(1125,625),
                                cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                    #putting name in centre
                    (w,h), _ = cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_DUPLEX,1,1) #gettong the sixe of name
                    offset = (414-w)//2 #414 is the total width of the inside img such as 1.png etc...
                    cv2.putText(imgBackground,str(studentInfo['name']),(808+offset,445),
                                cv2.FONT_HERSHEY_DUPLEX,1,(50,50,50),1)
                    imgBackground [175:175+216,909:909+216]= imgstudent
                    cv2.waitKey(250)
            counter+=1
            #resetting the counter for the next person
            if counter >= 20 :
                counter=0
                modeType=0
                studentInfo= []
                imgstudent=[]
                imgBackground[ 44:44+633, 808:808+414 ] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0

    cv2.imshow("Face-attendance",imgBackground)
    cv2.waitKey(1)
 