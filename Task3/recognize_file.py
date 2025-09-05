import cv2
import json
import os

MODEL_PATH = "model.yml"
LABELS_PATH = "labels.json"
CONFIDENCE_THRESHOLD = 61.0

def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(LABELS_PATH):
        print("Model or labels missing. Run train_recognizer.py first.")
        return None, None
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)
    with open(LABELS_PATH, "r") as f:
        labels = json.load(f)
    id_to_name = {v: k for k, v in labels.items()}
    return recognizer, id_to_name

def draw_prediction(frame, x, y, w, h, label_id, confidence, id_to_name):
    if confidence < CONFIDENCE_THRESHOLD:
        name = id_to_name.get(label_id, "Unknown")
        text = f"{name} ({confidence:.0f})"
        color = (0, 255, 0)
    else:
        text = "Unknown"
        color = (0, 0, 255)
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
    cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

def main():
    recognizer, id_to_name = load_model()
    if recognizer is None:
        return

    file_path = input("Enter image or video filename (with extension): ").strip().strip('\"')
    if not os.path.exists(file_path):
        print("❌ File not found! Provide full path or place file in this folder.")
        return

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    video_exts = {".mp4", ".avi", ".mov", ".mkv", ".wmv"}
    ext = os.path.splitext(file_path)[1].lower()

    if ext in image_exts:
        img = cv2.imread(file_path)
        if img is None:
            print("Could not read image.")
            return
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(80, 80))
        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (200, 200))
            label_id, conf = recognizer.predict(roi)
            draw_prediction(img, x, y, w, h, label_id, conf, id_to_name)
        cv2.imshow("Image Recognition", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif ext in video_exts:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            print("Could not open video.")
            return
        print("Press 'Q' or 'Esc' to quit.")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(80, 80))
            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                roi = cv2.resize(roi, (200, 200))
                label_id, conf = recognizer.predict(roi)
                draw_prediction(frame, x, y, w, h, label_id, conf, id_to_name)
            cv2.imshow("Video Recognition", frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord('q'), ord('Q'), 27):
                break
        cap.release()
        cv2.destroyAllWindows()

    else:
        print("❌ Unsupported file format! Use image (.jpg,.png,...) or video (.mp4,.avi,.mov,...)")

if __name__ == "__main__":
    main()
