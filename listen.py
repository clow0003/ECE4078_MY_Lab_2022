import socket
import cv2
import numpy as np
from AlphaBot import AlphaBot
from picamera import PiCamera
from bottle import Bottle, get, run, request

app = Bottle()

def setup_app(app):
    app.bot = AlphaBot()
    app.camera = PiCamera()
    app.camera.resolution = (640,480)
    app.camera.framerate = 24
        
setup_app(app)

@app.get("/camera/get")
def get_image():
    width, height = app.camera.resolution
    image = np.empty((height * width * 3,), dtype=np.uint8)
    app.camera.capture(image, 'bgr', use_video_port=True)
    image = image.reshape((height, width, 3))
    return cv2.imencode('.jpg', image)[1].tobytes()
    
@app.get('/robot/set/velocity')
def set_velocity():
    vel = request.query.value.split(',')
    app.bot.setMotor(int(vel[0]), int(vel[1]))


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(('8.8.8.8',80))
localhost=s.getsockname()[0]
run(app, host=localhost, port=8000)