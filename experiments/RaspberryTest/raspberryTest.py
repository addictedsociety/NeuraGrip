#!/usr/bin/env python3
import os
import time
import cv2
import RPi.GPIO as GPIO
from time import sleep
from LCD.PCF8574 import PCF8574_GPIO
from LCD.Adafruit_LCD1602 import Adafruit_CharLCD

# --- Display-Server setzen ---
os.environ["DISPLAY"] = ":0"  # Setzt den Display-Server für X11

# --- Globale Variablen ---
prev_x, prev_y = -1, -1  # Speichert vorherige Gesichtswerte

# --- GPIO-Pins für LEDs ---
ledPin_red = 17
ledPin_blue = 27
ledPin_green = 22

# --- Servo-Motor Einstellungen ---
OFFSET_DUTY = 0.5
SERVO_MIN_DUTY = 2.5 + OFFSET_DUTY
SERVO_MAX_DUTY = 12.5 + OFFSET_DUTY
SERVO_DELAY_SEC = 0.005
servoPin = 18

# --- LCD-Setup ---
PCF8574_address = 0x27
try:
    mcp = PCF8574_GPIO(PCF8574_address)
except:
    try:
        mcp = PCF8574_GPIO(0x3F)
    except:
        print("❌ I2C Address Error!")
        exit(1)

lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
mcp.output(3, 1)
lcd.begin(16, 2)
lcd.clear()
lcd.noBlink()
lcd.noCursor()

# --- Gesichtserkennung-Setup ---
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# --- Setup-Funktion ---
def setup():
    """Initialisiert GPIO, Servo und LCD."""
    GPIO.setmode(GPIO.BCM)

    # Servo-Pin setzen
    global p
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.output(servoPin, GPIO.LOW)
    p = GPIO.PWM(servoPin, 50)
    p.start(0)

    # LEDs setzen
    GPIO.setup(ledPin_red, GPIO.OUT)
    GPIO.setup(ledPin_blue, GPIO.OUT)
    GPIO.setup(ledPin_green, GPIO.OUT)
    GPIO.output(ledPin_red, GPIO.LOW)
    GPIO.output(ledPin_blue, GPIO.LOW)
    GPIO.output(ledPin_green, GPIO.LOW)

    lcd.display()

# --- Servo-Steuerung ---
def servoWrite(angle):
    """Dreht den Servo auf einen bestimmten Winkel (0-180 Grad)."""
    angle = max(0, min(angle, 180))
    dc = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * angle / 180.0
    p.ChangeDutyCycle(dc)

# --- Haupt-Loop ---
def loop():
    global prev_x, prev_y

    # Servo auf Startposition setzen
    servoWrite(90)
    sleep(0.5)

    # Kamera-Initialisierung
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FPS, 30)  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        print("❌ Kamera konnte nicht geöffnet werden!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame konnte nicht gelesen werden!")
            break

        # Bild in Graustufen konvertieren
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Gesichtserkennung mit optimierten Parametern
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Zeichne Bounding-Box um erkannte Gesichter
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            center_of_face = (x + w // 2, y + h // 2)
            cv2.circle(frame, center_of_face, 3, (0, 255, 0), -1)

        # LED-Steuerung basierend auf der Anzahl der Gesichter
        if len(faces) == 0:
            GPIO.output(ledPin_red, GPIO.HIGH)
            GPIO.output(ledPin_blue, GPIO.LOW)
            GPIO.output(ledPin_green, GPIO.LOW)
            print("😐 Kein Gesicht erkannt!")

        elif len(faces) == 1:
            GPIO.output(ledPin_red, GPIO.LOW)
            GPIO.output(ledPin_blue, GPIO.HIGH)
            GPIO.output(ledPin_green, GPIO.LOW)
            print("😊 Ein Gesicht erkannt!")

        else:
            GPIO.output(ledPin_red, GPIO.LOW)
            GPIO.output(ledPin_blue, GPIO.HIGH)
            GPIO.output(ledPin_green, GPIO.HIGH)
            print("😃 Mehrere Gesichter erkannt!")

        # LCD nur aktualisieren, wenn sich die Werte geändert haben
        if len(faces) > 0:
            center_of_face_x, center_of_face_y = center_of_face
            if center_of_face_x != prev_x or center_of_face_y != prev_y:
                lcd.clear()
                lcd.setCursor(0, 0)
                lcd.message(f"X:{center_of_face_x}  ")
                lcd.setCursor(0, 1)
                lcd.message(f"Y:{center_of_face_y}  ")
                prev_x, prev_y = center_of_face_x, center_of_face_y

        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"): # Str + C beenden
            break

# --- Aufräum-Funktion ---
def destroy():
    """Führt die notwendigen Aufräumarbeiten durch."""
    lcd.clear()
    mcp.output(3, 0)  # LCD-Backlight aus

    servoWrite(90)  # Servo auf 90° setzen
    time.sleep(0.5)
    p.stop()

    GPIO.cleanup()  # GPIO freigeben

# --- Skript starten ---
if __name__ == "__main__":
    print("🚀 Program is starting...\n")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()


# Oben Link (0,0) -> Rechts unten (640,480)