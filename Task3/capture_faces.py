import cv2
import os

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main():
    person_name = input("Enter person's name (no spaces recommended): ").strip()
    if not person_name:
        print("Name is required. Exiting.")
        return

    save_dir = os.path.join("dataset", person_name)
    ensure_dir(save_dir)

    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(cascade_path)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam. Make sure it's connected and not in use by another app.")
        return

    print("Controls: Press 'C' to capture, 'Q' or 'Esc' to quit.")
    count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Capture Faces - " + person_name, frame)
        key = cv2.waitKey(1) & 0xFF

        if key in (ord('c'), ord('C')):
            if len(faces) == 0:
                print("No face detected. Try again.")
                continue
            (x, y, w, h) = max(faces, key=lambda f: f[2]*f[3])
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            filename = os.path.join(save_dir, f"{person_name}_{count:04d}.jpg")
            cv2.imwrite(filename, face_img)
            count += 1
            print(f"Saved {filename}")

        if key in (ord('q'), ord('Q'), 27):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Done. Saved {count} images to {save_dir}")

if __name__ == "__main__":
    main()
