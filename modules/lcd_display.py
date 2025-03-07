
from LCD.Adafruit_LCD1602 import Adafruit_CharLCD
from LCD.PCF8574 import PCF8574_GPIO

class LCD:
    def __init__(self):
        self.PCF8574_address = 0x27
        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(0x3F)
            except:
                print("❌ I2C Address Error!")
                exit(1)

        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=self.mcp)
        self.mcp.output(3, 1)
        self.lcd.begin(16, 2)
        self.lcd.clear()
        self.lcd.noBlink()
        self.lcd.noCursor()

    def update(self, x, y):
        """Aktualisiert das LCD mit den X- und Y-Koordinaten."""
        self.lcd.clear()
        self.lcd.setCursor(0, 0)
        self.lcd.message(f"X:{x}  ")
        self.lcd.setCursor(0, 1)
        self.lcd.message(f"Y:{y}  ")
