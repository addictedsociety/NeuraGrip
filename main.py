import cv2
import os
from modules.servo_control import Servo
from modules.lcd_display import LCD
from modules.led_control import LED
from modules.face_detection import detect_faces


# --- Display-Server setzen ---
os.environ["DISPLAY"] = ":0"  # Setzt den Display-Server für X11

# Initialisierung der Servos, des LCDs und der LEDs
servo_x = Servo(18)
servo_y = Servo(19)
lcd = LCD()
led = LED(17, 27)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def loop() -> None:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame)
        led.update(faces)

        if faces:
            # Wähle das größte Gesicht (nach Fläche w*h)
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            face = faces[0]  # Nimm nur das größte Gesicht

            x, y, w, h = face
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            lcd.update(face_center_x, face_center_y)


        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

if __name__ == "__main__":
    print("NeuraGrip gestartet!")
    try:
        loop()
    except KeyboardInterrupt: # mit Str + C beenden 
        print("NeuraGrip beendet!")
    