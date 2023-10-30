from flask import Flask, render_template, Response, request,redirect
import cv2
from PIL import Image
import numpy as np
import io
import datetime
import mysql.connector
import json

from google.cloud import vision

from FaceCamera import FaceCamera
from PlateCamera import PlateCamera
from modeldeepface import *


dumy = cv2.imread(r"wajahcrop.png")
dumy1 = get_embedding(dumy)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'your_credentials.json'
gclient = vision.ImageAnnotatorClient()

app = Flask(__name__)

cam1 = cv2.VideoCapture(0)
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

cam2 = cv2.VideoCapture('rtsp://admin:admin@192.168.0.4:554/mode=real&idc=1&ids=1')
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

face_camera = FaceCamera(cam1)
plate_camera = PlateCamera(cam2)

def get_mid_last_plate(str_plate):
    tmp_noplat = ''
    tmp_kodeplat_blkng = ''
    str_plate = str_plate.lstrip()
    # print(str_plate)
    for i, v in enumerate(str_plate):
        if ' ' in v:
            str_plate = str_plate [i:]
            str_plate = str_plate.lstrip()
            tmp_kodeplat_blkng = str_plate
            break
        else:
            if v.isdigit:
                tmp_noplat = tmp_noplat + v
    return tmp_noplat,tmp_kodeplat_blkng

def OCR(img):
    kodeplat1 = ['K','R','G','H','D','F','E','Z'
    ,'T','A','B','L','M','N','S','W','P'
    ]
    kodeplat2 = ['AA','AD','AB','AG','AE','DK',
    'ED','EA','EB','DH','DR','KU','KT','DA','KB','KH','DC',
    'DD','DN','DT','DL','DM','DB','BA','BB','BD','BE','BG',
    'BH','BK','BL','BM','BN','BP','DE','DG','PA','PB'
    ]
    tmp_kodeplat =''
    tmp_noplat =''
    tmp_kodeplat_blkng =''

    image = vision.Image(content=img)
    text_data = []
    response_text = gclient.text_detection(image=image)
    for r in response_text.text_annotations:
        text_data.append(r.description)
    for nplt in text_data:
        if("\n" in nplt):
            head, sep, tail = nplt.partition('\n')
            nplt = head
        if(' ' in nplt):
            nplt = nplt.replace('.', '')
            if(nplt[:2].isalpha() and nplt[:2] in kodeplat2):
                tmp_kodeplat = nplt[:2]
                nplt = nplt[2:]
                tmp_noplat, tmp_kodeplat_blkng = get_mid_last_plate(nplt)
                return tmp_kodeplat,tmp_noplat,tmp_kodeplat_blkng
            elif(nplt[:1].isalpha() and nplt[:1] in kodeplat1):
                tmp_kodeplat = tmp_kodeplat + nplt[:1]
                nplt = nplt[1:]
                # print(nplt)
                # output  6370 LN
                tmp_noplat, tmp_kodeplat_blkng = get_mid_last_plate(nplt)
                return tmp_kodeplat,tmp_noplat,tmp_kodeplat_blkng
        else:
            if nplt.isalpha():
                if nplt in kodeplat1 or nplt in kodeplat2:
                    tmp_kodeplat = nplt
                else:
                    tmp_kodeplat_blkng = nplt
            elif nplt.isdigit():
                tmp_noplat = nplt
    return tmp_kodeplat,tmp_noplat,tmp_kodeplat_blkng


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        messages = ""
        bimg = plate_camera.get_croped_frame()
        
        img = Image.open(io.BytesIO(bimg))

        b = io.BytesIO()
        img.save(b, format='PNG')
        b.seek(0)

        depan, tengah, belakang = OCR(b.read())

        if len(depan) <= 0 or len(depan) > 2 or not depan.isalpha():
            messages = "22"
            return render_template('index.html',messages = messages)
        elif len(tengah) <= 0 or len(tengah) > 4 or not tengah.isalnum():
            messages = "22"
            return render_template('index.html',messages = messages)
        elif len(belakang) <= 0 or len(belakang) > 2 or not depan.isalpha():
            messages = "22"
            return render_template('index.html',messages = messages)

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "xrzqx"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM xrzqx.history where nomor = '" + depan + tengah + belakang +  "' and waktu_keluar is null"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if not myresult :
            str_plate = depan+tengah+belakang
            sign_in_timestamp = datetime.datetime.now()
            img_jpg = face_camera.get_img_face_align()
            img_emb = get_embedding(img_jpg)

            json_val = ', '.join(map(str, map(lambda x: f'"{x}"' if isinstance(x, str) else x, img_emb)))
            json_val = '[' + json_val + ']'
            json_val = '"{}"'.format(json_val)

            json_face = '{' + '"{}"'.format(0) + ":" + json_val + '}'

            sql = "INSERT INTO history (nomor,waktu_masuk,img_emb) VALUES (%s,%s,%s)"
            val = (str_plate,sign_in_timestamp,json_face)
            mycursor.execute(sql, val)
            mydb.commit()
            messages = "11"
        else:
            #plat nomor telah terdaftar
            messages = "00"
        mycursor.close()
        if(mydb.is_connected()):
            mydb.close()

        return render_template('index.html',messages = messages)
    else:
        return render_template('index.html')
    
@app.route('/keluar',methods=['GET','POST'])
def keluar():
    if request.method == 'POST':
        messages = ""
        bimg = plate_camera.get_croped_frame()
        
        img = Image.open(io.BytesIO(bimg))

        b = io.BytesIO()
        img.save(b, format='PNG')
        b.seek(0)

        depan, tengah, belakang = OCR(b.read())

        if len(depan) <= 0 or len(depan) > 2 or not depan.isalpha():
            messages = "22"
            return render_template('index.html',messages = messages)
        elif len(tengah) <= 0 or len(tengah) > 4 or not tengah.isalnum():
            messages = "22"
            return render_template('index.html',messages = messages)
        elif len(belakang) <= 0 or len(belakang) > 2 or not depan.isalpha():
            messages = "22"
            return render_template('index.html',messages = messages)

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "xrzqx"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM xrzqx.history where nomor = '" + depan + tengah + belakang +  "' and waktu_keluar is null"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        if not myresult :
            mycursor.close()
            if(mydb.is_connected()):
                mydb.close()
            messages = "2"
            return render_template('keluar.html',messages = messages)
        else:
            if len(myresult) < 2:
                img_jpg = face_camera.get_img_face_align()
                img_emb = get_embedding(img_jpg)

                resultrow = myresult[0]

                femb = resultrow[4]
                face_dict = json.loads(femb)
                femb_str = face_dict["0"]

                np_femb = np.fromstring(femb_str[1:len(femb_str)-1], dtype=np.float32, sep=', ')
                result = face_verify(img_emb,np_femb)

                if (result == True):
                    messages = "1"
                    resultid = str(resultrow[0])
                    sign_out_timestamp = str(datetime.datetime.now())
                    sql = "UPDATE xrzqx.history SET waktu_keluar = '" + sign_out_timestamp + "' WHERE idhistory = '"+ resultid +"'"
                    mycursor.execute(sql)
                    mydb.commit()
                else:
                    messages = "0"
        mycursor.close()
        if(mydb.is_connected()):
            mydb.close()
        return render_template('index.html',messages = messages)
    else:
        return render_template('index.html')


@app.route('/video_face')
def video_face():
    return Response(face_camera.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_plate')
def video_plate():
    return Response(plate_camera.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
