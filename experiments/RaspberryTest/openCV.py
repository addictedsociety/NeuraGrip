#!/usr/bin/env python3
import os
os.environ["DISPLAY"] = ":0"  # Setzt den Display-Server (X-Server) auf :0

import cv2

def main():
    cap = cv2.VideoCapture(0)  # Öffnet die Standardkamera
    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden!", flush=True)
        return

    print("Drücke 'q' im Video-Fenster, um das Programm zu beenden.", flush=True)

    while True:
        ret, frame = cap.read()  # Liest den nächsten Frame
        if not ret:
            print("Frame konnte nicht gelesen werden!", flush=True)
            break

        cv2.imshow("Video Feed", frame)  # Zeigt den Frame in einem Fenster an

        key = cv2.waitKey(30) & 0xFF  # Warte 30ms auf einen Tastendruck
        if key == ord('q'):
            print("Taste 'q' erkannt. Programm wird beendet.", flush=True)
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
