
---

# NeuraGrip

NeuraGrip ist ein OpenCV-basiertes System zur Gesichtserkennung und -verfolgung, das einen Roboterarm steuert. Es läuft auf einem Raspberry Pi und verwendet Servo-Motoren, um in Echtzeit auf erkannte Gesichter zu reagieren. Das Projekt kombiniert Computer Vision, maschinelles Lernen und Embedded Systems in einer modularen Architektur, die sich einfach erweitern lässt.

## Features
- **Gesichtserkennung**: Verwendet entweder OpenCVs deep learning-basierte Modelle oder Haar-Cascades zur Erkennung von Gesichtern.
- **Live Gesichtstracking**: Dynamische Verfolgung eines erkannten Gesichts und entsprechende Anpassung der Servo-Motoren.
- **Raspberry Pi Integration**: Optimiert für den Einsatz auf Raspberry Pi (z. B. Raspberry Pi 4B) mit angeschlossenem Kameramodul.
- **Servo-Steuerung**: Über GPIO (z. B. mit RPi.GPIO oder pigpio) wird ein Pan-Tilt-Mechanismus angesteuert.
- **Grafische Benutzeroberfläche (GUI)**: Anzeige des Live-Kamerafeeds mit Bounding-Boxen und Tracking-Daten.
- **Modulare Architektur**: Einfache Erweiterung um weitere Features wie Objekterkennung oder Personenidentifikation.

## Komponenten

### Hardware
- Raspberry Pi (z. B. Raspberry Pi 4B)
- Raspberry Pi Kamera-Modul oder USB-Webcam
- Pan-Tilt Servo-Mechanismus (z. B. 2 x SG90)
- Netzteil (5V, 2,5A oder höher empfohlen)
- GPIO-Verkabelung und -Verbinder

### Software
- **Betriebssystem**: Raspberry Pi OS oder ein anderes Linux-basiertes System
- **Programmiersprache**: Python 3
- **Wichtige Bibliotheken**:
  - OpenCV (`cv2`)
  - NumPy
  - RPi.GPIO oder pigpio (für die Servo-Steuerung)
  - dlib (optional, für fortgeschrittenes Tracking)
  - Tkinter oder PyQt (für die GUI)

## Installation

### 1. Raspberry Pi vorbereiten
Aktualisieren Sie zunächst Ihr System:
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Abhängigkeiten installieren
Installieren Sie OpenCV und weitere benötigte Python-Pakete:
```bash
sudo apt install python3-opencv python3-pip
pip3 install numpy RPi.GPIO pigpio dlib
```
Falls Sie PyQt für die GUI verwenden möchten:
```bash
pip3 install pyqt5
```

### 3. Kamera und GPIO aktivieren
Aktivieren Sie das Kameramodul über `raspi-config`:
```bash
sudo raspi-config
```
Wählen Sie **Interfacing Options > Camera** und aktivieren Sie diese. Stellen Sie sicher, dass auch I2C und SPI aktiviert sind, sofern benötigt.

### 4. Repository klonen
Klonen Sie das Repository und wechseln Sie in das Projektverzeichnis:
```bash
git clone https://github.com/yourusername/NeuraGrip.git
cd NeuraGrip
```

## Nutzung

### Gesichtserkennung und Tracking starten
Starten Sie das Hauptprogramm, das alle Module integriert:
```bash
python3 src/main.py
```
Dieses Skript:
- Erfasst Kamerabilder
- Erkennt Gesichter mittels OpenCV
- Zeichnet Bounding-Boxen um erkannte Gesichter
- Berechnet den Versatz des Gesichts von der Bildmitte und passt die Servo-Motoren entsprechend an

### Servo-Konfiguration anpassen
In der Datei `src/robot_control.py` können Sie die GPIO-Pins und Parameter für die Servo-Steuerung konfigurieren:
```python
pan_servo_pin = 17
tilt_servo_pin = 18
```
Passen Sie auch Geschwindigkeit und Winkelbegrenzungen nach Bedarf an.

### GUI starten
Falls eine grafische Benutzeroberfläche eingerichtet wurde, kann diese separat gestartet werden:
```bash
python3 gui.py
```
(Beachten Sie, dass sich die GUI-Implementierung je nach Projektversion an einem anderen Ort befinden kann.)

## Projektstruktur
Das Repository ist wie folgt strukturiert:

```
robot_arm_project/
├── models/                
│   ├── haarcascade_frontalface.xml   # Vorgefertigtes Modell für Gesichtserkennung
│   ├── custom_model.pth                # Optional: eigenes trainiertes Modell
├── src/                   
│   ├── camera.py          # OpenCV-Kamera-Handling
│   ├── face_detection.py  # Gesichtserkennung mit OpenCV oder DNN
│   ├── robot_control.py   # Steuerung des Roboterarms (Servo-Motoren)
│   ├── main.py            # Hauptprogramm, das alle Module verbindet
├── config/                
│   ├── settings.json      # Konfigurationsdatei für Projekteinstellungen
├── scripts/               
│   ├── setup.sh           # Installiert benötigte Abhängigkeiten
│   ├── test_camera.py     # Testet die Kamera-Funktionalität
│   ├── test_robot.py      # Testet die Steuerung des Roboterarms
├── logs/                  
│   ├── system.log         # Log-Dateien zur Fehlerbehebung
├── docs/                  
│   ├── README.md          # Detaillierte Projektübersicht und Setup-Anleitung
│   ├── architecture.md    # Erläuterung der Software-Architektur
├── requirements.txt       # Liste der benötigten Python-Pakete
├── .gitignore             # Dateien, die von Git ignoriert werden
├── LICENSE                # Lizenz (optional)
└── README.md              # Diese Hauptdokumentation
```

## Troubleshooting

### Kamera wird nicht erkannt
- Prüfen Sie, ob die Kamera korrekt angeschlossen und aktiviert ist:
  ```bash
  ls /dev/video0  # Sollte ein Gerät anzeigen
  vcgencmd get_camera  # Erwartetes Ergebnis: detected=1
  ```

### Servo reagiert nicht
- Vergewissern Sie sich, dass GPIO aktiviert ist und die richtigen Pins in `src/robot_control.py` konfiguriert wurden.

### Niedrige Bildrate
- Versuchen Sie, die Kameraauflösung in `src/face_detection.py` zu reduzieren:
  ```python
  cap.set(3, 320)
  cap.set(4, 240)
  ```

## Zukünftige Erweiterungen
- **Gesichtserkennung**: Erweiterung zur Personenidentifikation mittels vortrainierter Modelle.
- **Gestensteuerung**: Integration von Handgestenerkennung.
- **Sprachsteuerung**: Steuerung des Systems per Sprachbefehl.
- **Cloud-Integration**: Streaming von Daten an ein Web-Dashboard.

## Lizenz
Dieses Projekt ist unter der MIT License veröffentlicht. Beiträge und Anpassungen sind willkommen.

## Mitwirkende
- [Your Name](https://github.com/yourusername)

Für Fehlerberichte oder Verbesserungsvorschläge öffnen Sie bitte ein Issue oder senden Sie einen Pull Request.

---
