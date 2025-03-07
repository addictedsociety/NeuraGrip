import cv2
import os
from modules.servo_control import Servo
from modules.lcd_display import LCD
from modules.led_control import LED
from modules.face_detection import detect_faces

import RPi.GPIO as GPIO
GPIO.setwarnings(False)  # Deaktiviert die Warnungen



# --- Display-Server setzen ---
os.environ["DISPLAY"] = ":0"  # Setzt den Display-Server für X11

# Initialisierung der Servos, des LCDs und der LEDs
servo_x = Servo(18) # Servo X (Links/Rechts)
#servo_y = Servo(19) # Servo Y (Hoch/Runter)
lcd = LCD()
led = LED(27, 17)

cap_x = 320
cap_y = 240

# Kamera-Initialisierung
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Buffer reduzieren für weniger Verzögerung
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))  # Schnelleren Codec setzen
cap.set(cv2.CAP_PROP_FPS, 60)  # Setzt die FPS auf 60 (so hoch wie möglich)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_x)  # Höhere Auflösung = mehr Details
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_y)

def loop() -> None:
    
    print("Gesichtserkennung wird gestartet...🤖")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame)
        led.update(faces)

        if len(faces) > 0:
            # Wähle das größte Gesicht (nach Fläche w*h)
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True) # Berechne die Fläche des Gesichts
            face = faces[0]  # Nimm nur das größte Gesicht

            x, y, w, h = face
            face_center_x = x + w // 2
            face_center_y = y + h // 2

            lcd.update(face_center_x, face_center_y)
            
            # Kopie des Frames für die Transparenz
            overlay = frame.copy()

            # 🎯 Bounding Box auf dem Overlay zeichnen (Volle Deckkraft)
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), thickness=2)  # -1 = Gefüllt

            # 🎭 Transparenz anwenden (0.4 = 40% Deckkraft)
            alpha = 0.4  # Ändere den Wert zwischen 0 (komplett durchsichtig) und 1 (undurchsichtig)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

            # 🎯 Mittelpunkt als undurchsichtigen Punkt zeichnen
            cv2.circle(frame, (face_center_x, face_center_y), 3, (255, 0, 0), -1)  # Roter Punkt
            
        
            # 🎯 Servo X (Links/Rechts) anpassen
            error_x = face_center_x - (cap_x // 2)  # Abstand zur Bildmitte
            angle_x = 90 + (error_x / (cap_x // 2)) * 45  # Skaliere auf Servo-Winkelbereich
            servo_x.move(angle_x)
            
            # 🎯 **Servo Y (Hoch/Runter) anpassen**
            # error_y = face_center_y - (cap_y // 2)
            # angle_y = 90 - (error_y / (cap_y // 2)) * 45  # Skaliere auf Servo-Winkelbereich
            # servo_y.move(angle_y)
        

        frame = cv2.resize(frame, (1280, 960))

        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

def clear() -> None:
    """Setzt alle GPIO-Pins zurück und beendet das Programm."""
    GPIO.cleanup()
    cap.release()
    cv2.destroyAllWindows()
    lcd.reset()
    servo_x.stop()  
    


if __name__ == "__main__":
    print("NeuraGrip gestartet! 🚀")
    
    print("Drücke Str + C um NeuraGrip zu beenden.")
    
    try:
        loop()
    except KeyboardInterrupt: # mit Str + C beenden 
        clear()
        print("NeuraGrip beendet!")
    