import cv2
import numpy as np

class FaceCamera(object):
    def __init__(self, cam):
        self.video = cam
        self.web_width = 640
        self.web_height = 460
        (self.success, self.frame) = (None,None)
        self.frame_cp = None
        self.face_frame = None
        self.face_frame_align = None
        self.x, self.y, self.w, self.h = None,None,None,None

    def __del__(self):
        self.video.release()

    def get_frame_web(self,img):
        resized_image = cv2.resize(img, (self.web_width, self.web_height))
        _, buffer = cv2.imencode('.jpg', resized_image)
        image_data = buffer.tobytes()
        return image_data

    def gen(self):
        print("Waiting to open camera")
        while True:
            (self.success, self.frame) = self.video.read()
            self.frame_cp = self.frame.copy()
            if not self.success:
                break

            self.face_detection(img=self.frame_cp)
            self.eye_detection()
            frame = self.get_frame_web(img=self.frame_cp)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
    def face_detection(self,boxes=True,align=False, img=None):
        frame = img
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,1.5,5, minSize=(270,270))
        if len(faces) == 1:
            for (x,y,w,h) in faces:
                self.x, self.y, self.w, self.h = x,y,w,h
                self.face_frame = frame[y:y+h, x:x+w]
                if align:
                    self.face_frame_align = frame[y:y+h, x:x+w]
                if boxes:
                    cv2.rectangle(self.frame_cp, (x, y), (x + w, y + h), (0, 0, 255), 2)
        else:
            self.face_frame = None
            if align:
                self.face_frame_align = None
    
    def eye_detection(self):
        if(isinstance(self.face_frame,np.ndarray)):
            face_gray = cv2.cvtColor(self.face_frame, cv2.COLOR_BGR2GRAY)
            gray_left = face_gray[0:int(face_gray.shape[0]/2), 0:int(face_gray.shape[1]/2)]

            gray_right = face_gray[0:int(face_gray.shape[0]/2), int(face_gray.shape[1]/2):face_gray.shape[1]]

            blank_gray = np.zeros((int(self.face_frame.shape[0]/2), int(self.face_frame.shape[1]/2)), np.uint8)
            gray_merge_left= np.hstack((gray_left,blank_gray))
            gray_merge_right= np.hstack((blank_gray,gray_right))

            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyesleft = eye_cascade.detectMultiScale(gray_merge_left, 1.3, 3)
            eyesright = eye_cascade.detectMultiScale(gray_merge_right, 1.3, 3)
            # print(len(eyesleft), len(eyesright))

            if len(eyesright) == 1 and len(eyesleft) == 1:
                # center of right eye
                right_eye_center = (
                    int(eyesright[0][0] + (eyesright[0][2]/2)),
                    int(eyesright[0][1] + (eyesright[0][3]/2)))
                # center of left eye
                left_eye_center = (
                    int(eyesleft[0][0] + (eyesleft[0][2] / 2)),
                    int(eyesleft[0][1] + (eyesleft[0][3] / 2)))

                #doing eye aligment
                right_eye_x = right_eye_center[0]
                right_eye_y = right_eye_center[1]
                left_eye_x = left_eye_center[0]
                left_eye_y = left_eye_center[1]

                cv2.circle(self.frame_cp, (self.x+right_eye_x,self.y+right_eye_y), 3, (255, 0, 0), 2)
                cv2.circle(self.frame_cp, (self.x+left_eye_x,self.y+left_eye_y), 3, (255, 0, 0), 2)

                delta_x = right_eye_x - left_eye_x
                delta_y = right_eye_y - left_eye_y
                try:
                    angle=np.arctan(delta_y/delta_x)
                    angle = (angle * 180) / np.pi
                except:
                    angle = 0

                # Width and height of the image
                h, w = self.frame.shape[:2]
                # Calculating a center point of the image
                # Integer division "//"" ensures that we receive whole numbers
                center = (w // 2, h // 2)
                M = cv2.getRotationMatrix2D(center, (angle), 1.0)
                img = cv2.warpAffine(self.frame, M, (w, h))
                self.face_detection(boxes=False,align=True,img=img)
            else:
                self.face_frame_align = None
        else:
            self.face_frame_align=None

    def get_img_face_align(self):
        while True:
            if(isinstance(self.face_frame_align,np.ndarray)):
                img = self.face_frame_align
                return img

