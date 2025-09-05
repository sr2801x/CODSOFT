import cv2, json, os

MODEL_PATH = "model.yml"
LABELS_PATH = "labels.json"
CONFIDENCE_THRESHOLD = 70.0  # lower = stricter

def main():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        print("Model or labels missing. Run train_recognizer.py first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    with open(LABELS_PATH, "r") as f:
        label_map = json.load(f)
    id_to_name = {v: k for k, v in label_map.items()}

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    print("Press 'Q' or 'Esc' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))
            label_id, confidence = recognizer.predict(face)
            if confidence < CONFIDENCE_THRESHOLD:
                name = id_to_name.get(label_id, "Unknown")
                text = f"{name} ({confidence:.0f})"
                color = (0, 255, 0)
            else:
                text = "Unknown"
                color = (0, 0, 255)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Real-time Face Recognition", frame)
        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q'), 27):  # Esc=27
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
