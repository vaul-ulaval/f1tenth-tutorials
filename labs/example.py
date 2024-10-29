#!/usr/bin/env python

import autodrive
import eventlet
import numpy as np
import socketio
from flask import Flask

# Autodrive constants
VERBOSE_OUTPUT = False

# Car constants
LIDAR_FOV_DEGREE = 270
MAX_SPEED = 4.92 # m/s


# Vehicle and server init
f1tenth = autodrive.F1TENTH()
f1tenth.id = 'V1'
sio = socketio.Server()
app = Flask(__name__)


def send_control_command(throttle: float, steering: float):
    f1tenth.throttle_command = np.clip(throttle, -1, 1) # [-1, 1]
    f1tenth.steering_command = np.clip(steering, -1, 1) # [-1, 1]

    json_msg = f1tenth.generate_commands(verbose=VERBOSE_OUTPUT) # Generate vehicle 1 message

    try:
        sio.emit('Bridge', data=json_msg)
    except Exception as exception_instance:
        print(exception_instance)


# Registering "connect" event handler for the server
@sio.on('connect')
def connect(sid, environ):
    print('Connected!')


# Registering "Bridge" event handler for the server
@sio.on('Bridge')
def bridge(sid, data):
    if not data:
        return

    f1tenth.parse_data(data, verbose=VERBOSE_OUTPUT)

    throttle = 1.0 # [-1.0, 1.0]
    steering = 1.0 # [-1.0, 1.0]

    send_control_command(throttle, steering)


if __name__ == '__main__':
    app = socketio.Middleware(sio, app) # Wrap flask application with socketio's middleware
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app) # Deploy as an eventlet WSGI server