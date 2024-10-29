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
THETA_DEG = 45
LOOKAHEAD = 1.0 # m
DESIRED_DISTANCE_FROM_WALL = 0.8 # m
INTEGRAL_WINDOW_SIZE = 10
KP = 0.8
KD = 0.0
KI = 0.0


# Lab variables
f1tenth = autodrive.F1TENTH()
f1tenth.id = 'V1'

# Server init
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


def is_valid_lidar_scan(scan: float) -> bool:
    return not math.isinf(scan) and not math.isnan(scan)


# Registering "connect" event handler for the server
@sio.on('connect')
def connect(sid, environ):
    print('Connected!')


# Registering "Bridge" event handler for the server
@sio.on('Bridge')
def bridge(sid, data):
    if not 'last_time' in globals():
        global last_time, last_steering, last_errors_window
        last_time = None
        last_steering = 0.0
        last_errors_window = np.array([])

    if not data:
        return

    steering = 0.0 # [-1.0, 1.0]
    throttle = 0.3 # [-1.0, 1.0]

    f1tenth.parse_data(data, verbose=VERBOSE_OUTPUT)

    theta = np.radians(THETA_DEG)
    theta_b = -np.pi/2.0
    theta_a = theta_b + theta
    a = angle_to_distance(theta_a, f1tenth.lidar_range_array)
    b = angle_to_distance(theta_b, f1tenth.lidar_range_array)

    if not is_valid_lidar_scan(a) or not is_valid_lidar_scan(b):
        print("Invalid lidar scan, repeating last command")
        send_control_command(throttle, last_steering)
        return

    alpha = math.atan((a*math.cos(theta) - b)/(a*math.sin(theta)))
    D_t = b*math.cos(alpha)
    D_tp1 = D_t + LOOKAHEAD*math.sin(alpha)

    error = DESIRED_DISTANCE_FROM_WALL - D_tp1

    # PID control
    if last_time is None:
        error_diff = 0.0
        error_integral = 0.0
    else:
        dt = time.time() - last_time
        de = error - last_errors_window[-1]
        error_diff = de / dt
        error_integral = np.sum(last_errors_window) * dt

    steering = error*KP + error_integral*KI + error_diff*KD

    # Updating variables
    last_steering = steering
    last_time = time.time()
    if len(last_errors_window) >= INTEGRAL_WINDOW_SIZE:
        last_errors_window[:-1] = last_errors_window[1:]
        last_errors_window[-1] = error
    else:
        last_errors_window = np.append(last_errors_window, error)

    send_control_command(throttle, steering)


if __name__ == '__main__':
    app = socketio.Middleware(sio, app) # Wrap flask application with socketio's middleware
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app) # Deploy as an eventlet WSGI server