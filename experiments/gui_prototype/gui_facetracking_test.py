import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

class FaceTrackingTest:
    def __init__(self, window):
        self.window = window
        self.window.title("Face Tracking Test")
        self.window.geometry("1280x720")

        self.count_faces = 0
        
        # VideoCapture einrichten
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        # Haar-Cascade laden
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Haupt-Frame, das den gesamten Fensterbereich einnimmt
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(expand=True, fill="both")
        
        # Label für das Video, per place() mittig positioniert
        self.video_label = ctk.CTkLabel(self.main_frame, width=640, height=480, text="", corner_radius=10)
        
        # Richtig: ohne zusätzlichen Text in den Parametern
        self.video_label.place(relx=0.5, rely=0.5, anchor='center')  # Platziert das Widget in der Mitte


        # Frame-Update starten
        self.update_frame()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Gesichtserkennung
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30,30))
            
            # Anzahl erkannter Gesichter ermitteln
            self.count_faces = len(faces)
            cv2.putText(frame, f"Faces: {self.count_faces}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Gefundene Gesichter markieren
            for (x, y, w, h) in faces:
                center = (x + w // 2, y + h // 2)
                radius = int(0.5 * max(w, h))
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                cv2.line(frame, (x + w // 2, y), (x + w // 2, y + h), (0, 255, 0), 2)
                cv2.line(frame, (x, y + h // 2), (x + w, y + h // 2), (0, 255, 0), 2)
                cv2.circle(frame, center, 5, (255, 0, 0), -1)
                
                
                # - Mittelpunkt des Gesichts berechnen -s
                x_mitte = x + w//2
                y_mitte = y + h//2                
                # Koordinaten des Mittelpunktes anzeigen
                text = f'Mittelpunkte Gesicht: ({x_mitte}, {y_mitte})'	    
                # cv2.putText(Bild, Text, Position, Schriftart, Skalierung, Farbe(BGR), Dicke)
                cv2.putText(frame, text, (20,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            
            # Bild für Tkinter konvertieren
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=image)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        
        # Nächsten Frame nach 10ms updaten
        self.window.after(10, self.update_frame)
        
    def on_closing(self):
        if self.cap.isOpened():
            self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = FaceTrackingTest(root)
    root.mainloop()
