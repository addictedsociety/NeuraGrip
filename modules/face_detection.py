import cv2

# Lade das LBP-Modell für die Gesichtserkennung (schneller als Haarcascades)
face_cascade = cv2.CascadeClassifier("models/lbpcascade_frontalface.xml")

def detect_faces(frame):
    """Erkennt Gesichter im Bild mit LBP und gibt Bounding-Boxes zurück."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # In Graustufen umwandeln
    faces = face_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50)
    )
    
    return faces  # Gibt eine Liste mit Bounding-Box-Koordinaten zurück

