from website import create_app
import RPi.GPIO as GPIO

app = create_app()

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    finally:
        GPIO.cleanup()