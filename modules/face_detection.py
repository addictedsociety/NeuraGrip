import cv2

# Lade das Gesichtserkennungsmodell
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def detect_faces(frame):
    """Erkennt Gesichter im Bild und gibt die Bounding-Box zurück."""
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray_frame, scaleFactor=1.2, minNeighbors=3, minSize=(50, 50), flags=cv2.CASCADE_SCALE_IMAGE
    )
    return faces
