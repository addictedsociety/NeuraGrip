import RPi.GPIO as GPIO

class LED:
    def __init__(self, red_pin,green_pin):
        self.red = red_pin
        self.green = green_pin

        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)

    def update(self, faces):
        """Schaltet die LEDs basierend auf der Anzahl der erkannten Gesichter."""
        if len(faces) == 0:
            GPIO.output(self.red, GPIO.HIGH)
            GPIO.output(self.blue, GPIO.LOW)
            GPIO.output(self.green, GPIO.LOW)
        else:
            GPIO.output(self.red, GPIO.LOW)
            GPIO.output(self.green, GPIO.HIGH)
        
