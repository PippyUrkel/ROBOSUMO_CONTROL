from flask import Blueprint, render_template, request, jsonify
from BTS7960_MotorDriver import BTS7960_MotorDriver
import RPi.GPIO as GPIO
import threading
import time

views = Blueprint('views', __name__)

# Disable GPIO warnings
GPIO.setwarnings(False)

# Set GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Initialize the motor drivers
right_motor = BTS7960_MotorDriver(R_EN=21, L_EN=22, RPWM=23, LPWM=24)
left_motor = BTS7960_MotorDriver(R_EN=25, L_EN=26, RPWM=27, LPWM=28)

# Set up LED
# LED_PIN = 17  # Changed to 17 as per the error message
# GPIO.setup(LED_PIN, GPIO.OUT)

def blink_led(duration=1, blink_count=5):
    # Set GPIO mode inside the thread
    # GPIO.setmode(GPIO.BCM)
    # for _ in range(blink_count):
    #     GPIO.output(LED_PIN, GPIO.HIGH)
    #     time.sleep(duration / (2 * blink_count))
    #     GPIO.output(LED_PIN, GPIO.LOW)
    #     time.sleep(duration / (2 * blink_count))
    pass

@views.route('/')
def home():
    return render_template("base.html")

@views.route('/control_motor', methods=['GET'])
def control_motor():
    command = request.args.get('command')
    speed = int(request.args.get('speed', 50))  # Default speed is 50

    # Adjust speed if needed
    right_motor.set_speed(speed)
    left_motor.set_speed(speed)

    try:
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
        elif command == 'adjust_speed':
            # Just adjust the speed without changing direction
            pass
        else:
            return jsonify({'status': 'error', 'message': 'Invalid command'}), 400

        # Blink LED in a separate thread
        threading.Thread(target=blink_led).start()

        return jsonify({'status': 'success', 'command': command, 'speed': speed})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@views.route('/blink_led', methods=['GET'])
def trigger_led_blink():
    duration = float(request.args.get('duration', 1))
    blink_count = int(request.args.get('blink_count', 5))
    
    threading.Thread(target=blink_led, args=(duration, blink_count)).start()
    
    return jsonify({'status': 'success', 'message': 'LED blinking initiated'})

@views.teardown_app_request
def cleanup_gpio(exception=None):
    GPIO.cleanup()