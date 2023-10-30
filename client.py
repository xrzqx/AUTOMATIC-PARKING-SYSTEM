from flask import Flask, render_template, Response, request,redirect
import cv2

from FaceCamera import FaceCamera
import numpy as np

# from modeldeepface import *
# import json

app = Flask(__name__)

cam1 = cv2.VideoCapture(0)
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

face_camera = FaceCamera(cam1)

@app.route('/',methods=['GET'])
def index():
    return render_template('webcam.html')

@app.route('/sign_in',methods=['POST'])
def sign_in():
    if request.method == 'POST':
        img_jpg = face_camera.get_img_face_align()
        return redirect('/')

@app.route('/video_face')
def video_face():
    return Response(face_camera.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
