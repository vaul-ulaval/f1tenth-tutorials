#!/usr/bin/env python

import math
import time

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

# Lab constants
TTC_THRESOLD = 1.0 # s


# Vehicle and server init
f1tenth = autodrive.F1TENTH()
f1tenth.id = 'V1'
sio = socketio.Server()
app = Flask(__name__)


def angle_to_distance(theta_rad: float, lidar_array: list[float]):
    angle_min = math.radians(-LIDAR_FOV_DEGREE/2.0)
    angle_increment = math.radians(LIDAR_FOV_DEGREE/len(lidar_array))

    index = int((theta_rad-angle_min)/angle_increment)
    distance = lidar_array[index]

    return distance


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

    throttle = 0.2
    steering = 0.0

    speed = throttle * MAX_SPEED
    forward_distance = angle_to_distance(theta_rad=0, lidar_array=f1tenth.lidar_range_array)

    # If its a bad lidar reading
    if math.isnan(forward_distance) or math.isinf(forward_distance):
        send_control_command(throttle, steering)
        return

    ttc = forward_distance/speed
    if ttc < TTC_THRESOLD:
        print("Sending brake command")
        throttle = 0.0

    send_control_command(throttle, steering)


if __name__ == '__main__':
    app = socketio.Middleware(sio, app) # Wrap flask application with socketio's middleware
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app) # Deploy as an eventlet WSGI server