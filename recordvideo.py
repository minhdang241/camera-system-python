import numpy as np
import os
import socketio
import base64
import cv2
import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(11, GPIO.IN)

sio = socketio.Client()
sio.connect('http://172.20.10.4:8000')

filename = 'video'
frames_per_second = 24.0
res = '720p'


# Set resolution for the video capture
# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}


# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']




cap = cv2.VideoCapture(0)
order = 0
out = 0
name =''

while True:
    i = GPIO.input(11)
    print(i)
    ret, frame = cap.read()
    reval, buffer = cv2.imencode('.jpeg', frame)
    encoded_string = base64.b64encode(buffer)
    image = encoded_string.decode('utf-8')
    sio.emit('image', image)
    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
   
    if (i==1):
        if (out == 0):
            t = time.ctime(time.time())
            name = filename + t + '.mp4';
            out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'x264'),12, (640, 480))
        out.write(frame) 
    else:
        if (out != 0):
            out.release()
            out = 0
#            files = {'video': open(name, 'rb')}
#            response = requests.post('http://172.20.10.4:8000/upload', files=files)
            print(response.text)
    
cap.release()
out.release()
cv2.destroyAllWindows()

