# AUTOMATIC PARKING SYSTEM
The system is built on a web application by using flask and Google Vision API for text detection and recognition.
The system also uses [DeepFace model architecture](https://research.facebook.com/publications/deepface-closing-the-gap-to-human-level-performance-in-face-verification/) for face recognition and Haar Cascade Classifier Algorithm for face detection using OpenCV library

## Running Apps Local Deployment (Flask)
Step 1: Change Your Google Credentials in `client.py` file
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_credentials.json'
```
Step 2: Change Your Camera Setup in `client.py` file
```
cam1 = cv2.VideoCapture(0)
cam2 = cv2.VideoCapture('...')
```
Step 3: Run `client.py` file

## Demonstration of application
https://youtu.be/XV-N3Okb4Is

NOTE: THIS REPO IS SCHOOL ASSIGNMENT (THESIS)
