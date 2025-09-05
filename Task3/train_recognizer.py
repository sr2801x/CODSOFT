import os, json
import cv2
import numpy as np

DATASET_DIR = "dataset"
MODEL_PATH = "model.yml"
LABELS_PATH = "labels.json"

def load_images_and_labels():
    X, y = [], []
    label_map = {}
    next_label = 0

    for name in sorted(os.listdir(DATASET_DIR)):
        person_dir = os.path.join(DATASET_DIR, name)
        if not os.path.isdir(person_dir):
            continue
        if name not in label_map:
            label_map[name] = next_label
            next_label += 1

        for file in sorted(os.listdir(person_dir)):
            if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            path = os.path.join(person_dir, file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            img = cv2.resize(img, (200, 200))
            X.append(img)
            y.append(label_map[name])

    return X, y, label_map

def main():
    if not os.path.exists(DATASET_DIR):
        print("No dataset directory found. Run capture_faces.py first.")
        return

    X, y, label_map = load_images_and_labels()
    if len(X) == 0:
        print("No training images found. Run capture_faces.py first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(X, np.array(y))
    recognizer.write(MODEL_PATH)

    with open(LABELS_PATH, "w") as f:
        json.dump(label_map, f)

    print(f"Trained on {len(X)} images. Saved model to {MODEL_PATH} and labels to {LABELS_PATH}.")
    print("Labels:", label_map)

if __name__ == "__main__":
    main()
