# Face Attendance System

Welcome to the **Face Attendance System**!  
This project leverages facial recognition technology to automate and streamline the process of marking attendance. Built with Python, OpenCV, Flask, and Firebase, it provides a modern, user-friendly interface for both students and administrators.

---

## 🚀 Features

- **Real-Time Face Recognition:**  
  Detects and recognizes faces from a webcam feed in real time.

- **Automated Attendance Logging:**  
  Marks attendance automatically upon successful face recognition.

- **Firebase Integration:**  
  Stores student data and attendance records securely in Firebase Realtime Database and Storage.

- **Web Interface:**  
  Start and stop the camera easily from a beautiful web dashboard.

- **Visual Feedback:**  
  Modern UI overlays and feedback for recognized faces and attendance status.

---

## 🗂️ Project Structure

```
.
├── AddDataToDatabase.py         # Script to add student data to Firebase
├── EncodeGenerator.py           # Generates face encodings and uploads images to Firebase
├── EncodeFile.p                 # Pickle file storing face encodings and IDs
├── faceattendancesystem-srk-firebase-adminsdk-eh0jr-0cdc5c2e1f.json # Firebase credentials
├── main.py                      # Main face recognition and attendance marking script
├── mainfe.py                    # Alternate frontend script for face recognition
├── mainfe.log                   # Log file for debugging
├── run.py                       # Flask web server
├── Images/                      # Folder containing student images
├── Resources/
│   ├── background.png           # Background image for UI
│   └── Modes/                   # Mode images for UI feedback
├── templates/
│   └── index.html               # Web dashboard template
└── .vscode/
    └── settings.json            # VSCode settings
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/face-attendance-system.git
cd face-attendance-system
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed.

```sh
pip install -r requirements.txt
```

**Main dependencies:**
- opencv-python
- face_recognition
- numpy
- firebase-admin
- flask
- cvzone

### 3. Firebase Setup

- Create a Firebase project.
- Download the service account key JSON and place it in the project root.
- Update the credential path in scripts if necessary.

### 4. Add Student Data

- Place student images (named with their registration numbers, e.g., `201098.png`) in the `Images/` folder.
- Run [`EncodeGenerator.py`](EncodeGenerator.py) to generate face encodings and upload images to Firebase.
- Run [`AddDataToDatabase.py`](AddDataToDatabase.py) to add student details to Firebase.

### 5. Start the Web Server

```sh
python run.py
```

- Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)
- Use the web interface to start or stop the camera.

---

## 🖥️ How It Works

1. **Face Encoding:**  
   Student images are encoded and stored using [`EncodeGenerator.py`](EncodeGenerator.py).

2. **Attendance Marking:**  
   When the camera is started, [`mainfe.py`](mainfe.py) runs, recognizing faces in real time and updating attendance in Firebase.

3. **Web Dashboard:**  
   The Flask app ([`run.py`](run.py)) serves a modern dashboard ([`templates/index.html`](templates/index.html)) to control the camera and view status.

---

## 📝 Customization

- **UI Images:**  
  Change images in `Resources/background.png` and `Resources/Modes/` for a personalized look.
- **Attendance Interval:**  
  Adjust the attendance interval in [`main.py`](main.py) by changing the `secondsElapsed` threshold.

---

## 🤝 Contributing

Pull requests are welcome!  
For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [Firebase](https://firebase.google.com/)
- [cvzone](https://www.cvzone.com/)

---

**Made with
