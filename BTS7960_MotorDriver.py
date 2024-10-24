import RPi.GPIO as GPIO
import time

class BTS7960_MotorDriver:
    def __init__(self, R_EN, L_EN, RPWM, LPWM, speed=50):
        # Set up GPIO mode (BOARD: physical pin numbering)
        GPIO.setmode(GPIO.BOARD)
        
        # Define motor driver pins for each motor
        self.R_EN = R_EN  # Right enable pin
        self.L_EN = L_EN  # Left enable pin
        self.RPWM = RPWM  # Right PWM pin (for forward)
        self.LPWM = LPWM  # Left PWM pin (for reverse)
        
        # Set up GPIO pins
        GPIO.setup(self.R_EN, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.RPWM, GPIO.OUT)
        GPIO.setup(self.LPWM, GPIO.OUT)
        
        # Set enable pins to high to activate the motor driver
        GPIO.output(self.R_EN, True)  # Enable forward control
        GPIO.output(self.L_EN, True)  # Enable reverse control
        
        # Set up PWM with frequency of 1000 Hz (1 kHz)
        self.pwm_r = GPIO.PWM(self.RPWM, 1000)
        self.pwm_l = GPIO.PWM(self.LPWM, 1000)
        
        # Start PWM with 0% duty cycle (motor off initially)
        self.pwm_r.start(0)
        self.pwm_l.start(0)

        # Set a universal speed (default is 50%)
        self.speed = speed

    def set_speed(self, speed):
        """Set a universal speed for all movements."""
        self.speed = speed

    def forward(self):
        """Move the motor forward at the universal speed."""
        self.pwm_r.ChangeDutyCycle(self.speed)  # Set forward PWM duty cycle
        self.pwm_l.ChangeDutyCycle(0)           # Stop reverse motion

    def reverse(self):
        """Move the motor in reverse at the universal speed."""
        self.pwm_r.ChangeDutyCycle(0)           # Stop forward motion
        self.pwm_l.ChangeDutyCycle(self.speed)  # Set reverse PWM duty cycle

    def stop(self):
        """Stop the motor."""
        self.pwm_r.ChangeDutyCycle(0)           # Stop forward motion
        self.pwm_l.ChangeDutyCycle(0)           # Stop reverse motion

    def move_left(self):
        """Move left by rotating the left motor backward and right motor forward."""
        self.pwm_r.ChangeDutyCycle(self.speed)  # Move the right motor forward
        self.pwm_l.ChangeDutyCycle(self.speed)  # Move the left motor backward

    def move_right(self):
        """Move right by rotating the right motor backward and left motor forward."""
        self.pwm_r.ChangeDutyCycle(self.speed)  # Move the right motor backward
        self.pwm_l.ChangeDutyCycle(0)           # Stop the left motor (no reverse motion)

    def cleanup(self):
        """Clean up GPIO pins."""
        self.pwm_r.stop()
        self.pwm_l.stop()
        GPIO.cleanup()


# Example usage for controlling both left and right motors
if __name__ == "__main__":
    # Right motor driver (pins for right motor)
    right_motor = BTS7960_MotorDriver(R_EN=21, L_EN=22, RPWM=23, LPWM=24)
    
    # Left motor driver (pins for left motor)
    left_motor = BTS7960_MotorDriver(R_EN=25, L_EN=26, RPWM=27, LPWM=28)

    # Set a universal speed (optional, default is 50%)
    right_motor.set_speed(75)
    left_motor.set_speed(75)

    try:
        # Move both motors forward
        print("Moving forward...")
        right_motor.forward()
        left_motor.forward()
        time.sleep(3)

        # Stop both motors
        print("Stopping...")
        right_motor.stop()
        left_motor.stop()
        time.sleep(1)

        # Turn left
        print("Turning left...")
        left_motor.move_left()
        right_motor.forward()  # Keep the right motor moving forward
        time.sleep(3)

        # Turn right
        print("Turning right...")
        right_motor.move_right()
        left_motor.forward()   # Keep the left motor moving forward
        time.sleep(3)

        # Stop both motors again
        print("Stopping...")
        right_motor.stop()
        left_motor.stop()

    finally:
        # Clean up GPIO when done
        print("Cleaning up...")
        right_motor.cleanup()
        left_motor.cleanup()
