import RPi.GPIO as GPIO

class BTS7960_MotorDriver:
    def __init__(self, R_EN, L_EN, RPWM, LPWM, speed=50):
        # Set GPIO mode to BCM
        GPIO.setmode(GPIO.BCM)
    def __init__(self, R_EN, L_EN, RPWM, LPWM, speed=50):
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