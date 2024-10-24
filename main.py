from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Initialize motor driver class here (left and right motors)
from BTS7960_MotorDriver import BTS7960_MotorDriver

right_motor = BTS7960_MotorDriver(R_EN=21, L_EN=22, RPWM=23, LPWM=24)
left_motor = BTS7960_MotorDriver(R_EN=25, L_EN=26, RPWM=27, LPWM=28)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move_robot():
    data = request.json
    direction = data.get('direction')
    speed = data.get('speed', 0)

    # Move based on the direction
    if direction == 'forward':
        right_motor.forward(speed)
        left_motor.forward(speed)
    elif direction == 'reverse':
        right_motor.reverse(speed)
        left_motor.reverse(speed)
    elif direction == 'left':
        right_motor.forward(speed)
        left_motor.stop()
    elif direction == 'right':
        right_motor.stop()
        left_motor.forward(speed)
    elif direction == 'stop':
        right_motor.stop()
        left_motor.stop()

    return jsonify({"status": "OK", "direction": direction})

@app.route('/set_speed', methods=['POST'])
def set_speed():
    data = request.json
    speed = data.get('speed', 0)
    # You can store this speed in a global variable if needed, or adjust the motor speed accordingly
    return jsonify({"status": "OK", "speed": speed})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
