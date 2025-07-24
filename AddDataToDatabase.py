import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate(r"D:\Attendace_system_EE\faceattendancesystem-srk-firebase-adminsdk-eh0jr-0cdc5c2e1f.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-srk-default-rtdb.firebaseio.com/"
})

ref = db.reference("Students")
#data to be  added in firebase db
data = {
     "201098":
        {
            "name": "Siv Raam Krishnan.K.V",
            "major": "AI&DS",
            "starting_year": 2022,
            "total_attendance": 7,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
        "321654":
        {
            "name": "Murtaza Hassan",
            "major": "Robotics",
            "starting_year": 2017,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2022-12-11 00:54:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2022-12-11 00:54:34"
        }
}
#sending to the db
for key, value in data.items():
    ref.child(key).set(value)
