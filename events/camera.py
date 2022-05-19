import cv2
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        try:
            
            ret, frame = self.cap.read()
            frame_flip = cv2.flip(frame, 1)
            #ret, frame = cv2.imencode('.jpg', frame_flip)
            #ret, frame = cv2.read()
            return frame.tobytes()
        except Exception as E:
            print(E.__class__.__name__, str(E))