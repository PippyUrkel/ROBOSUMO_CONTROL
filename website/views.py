from flask import Blueprint, request, jsonify
from BTS7960_MotorDriver import BTS7960_MotorDriver

views = Blueprint('views', __name__)

# Initialize the motor drivers (assuming 2 motors)
right_motor = BTS7960_MotorDriver(R_EN=21, L_EN=22, RPWM=23, LPWM=24)
left_motor = BTS7960_MotorDriver(R_EN=25, L_EN=26, RPWM=27, LPWM=28)

@views.route('/control_motor', methods=['POST'])
def control_motor():
    data = request.get_json()
    command = data.get('command')
    speed = int(data.get('speed', 50))  # Default speed is 50

    # Adjust speed if needed
    right_motor.set_speed(speed)
    left_motor.set_speed(speed)

    if command == 'forward':
        right_motor.forward()
        left_motor.forward()
    elif command == 'reverse':
        right_motor.reverse()
        left_motor.reverse()
    elif command == 'left':
        right_motor.forward()
        left_motor.reverse()
    elif command == 'right':
        right_motor.reverse()
        left_motor.forward()
    elif command == 'stop':
        right_motor.stop()
        left_motor.stop()

    return jsonify({'status': 'success', 'command': command, 'speed': speed})
