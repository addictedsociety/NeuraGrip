import RPi.GPIO as GPIO
from time import sleep

SERVO_MIN_DUTY = 2.5
SERVO_MAX_DUTY = 12.5

class Servo:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, 50)
        self.pwm.start(0)

    def move(self, angle):
        """Dreht den Servo auf den angegebenen Winkel (0-180 Grad)."""
        angle = max(0, min(angle, 180))
        duty = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0
        self.pwm.ChangeDutyCycle(duty)
        sleep(0.05)

    def stop(self):
        self.pwm.stop()
