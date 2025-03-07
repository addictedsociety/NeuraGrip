
from .LCD.Adafruit_LCD1602 import Adafruit_CharLCD
from .LCD.PCF8574 import PCF8574_GPIO


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
        self.lcd.noBlink()
        self.lcd.noCursor()

        # Letzte Werte speichern
        self.last_x = None
        self.last_y = None

        # Einmalig das Label "X:" und "Y:" setzen (bleibt dauerhaft auf dem Display)
        self.lcd.setCursor(0, 0)
        self.lcd.message("X:")
        self.lcd.setCursor(0, 1)
        self.lcd.message("Y:")

    def update(self, x, y) -> None:
        """Überschreibt nur die Zahlenwerte auf dem LCD, anstatt das ganze Display zu löschen."""
        
        if x != self.last_x:
            self.lcd.setCursor(2, 0)  # Direkt nach "X:"
            self.lcd.message(f"{x}    ")  # Überschreibt alte Zahlen mit Leerzeichen, falls nötig
            self.last_x = x

        if y != self.last_y:
            self.lcd.setCursor(2, 1)  # Direkt nach "Y:"
            self.lcd.message(f"{y}    ")
            self.last_y = y

    def reset(self):
        self.lcd.clear() # Löscht das Display
        self.lcd.noDisplay() # Schaltet das Display aus
        self.mcp.output(3, 0) # Schaltet die Hintergrundbeleuchtung aus
        