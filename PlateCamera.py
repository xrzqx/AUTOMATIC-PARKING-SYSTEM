import cv2

class PlateCamera(object):
    def __init__(self, cam):
        self.video = cam
        self.web_width = 640
        self.web_height = 460
        (self.success, self.frame) = (None,None)
        self.frame_cp = None

    def __del__(self):
        self.video.release()

    def get_frame_web(self,img):
        resized_image = cv2.resize(img, (self.web_width, self.web_height))
        _, buffer = cv2.imencode('.jpg', resized_image)
        image_data = buffer.tobytes()
        return image_data
    
    def get_croped_frame(self):
        crop_img = self.frame[360:720, 30:1250]
        _, buffer = cv2.imencode('.jpg', crop_img)
        image_data = buffer.tobytes()
        return image_data

    def gen(self):
        print("Waiting to open camera")
        while True:
            (self.success, self.frame) = self.video.read()
            self.frame_cp = self.frame.copy()
            if not self.success:
                break

            start_point = (30, 360)
            end_point = (1250, 720)

            cv2.rectangle(self.frame_cp, start_point, end_point, (0, 255, 0), 2)
            frame = self.get_frame_web(img=self.frame_cp)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            