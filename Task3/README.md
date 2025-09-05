# Face Detection & Recognition — Ready Project (Windows/Mac/Linux)

This project detects and recognizes faces from **webcam**, **images**, or **video files** using OpenCV:
- **Detection:** Haar Cascade (pretrained)
- **Recognition:** LBPH (OpenCV's Local Binary Patterns Histogram)

> Simple, offline, great for demos/assignments. For production, consider ArcFace/InsightFace.

---

## 🔧 Quick Start (Windows)
1) Double-click `setup_windows.bat` (or run it) — it creates `.venv` and installs deps.  
2) Double-click `run_capture.bat` to collect face photos.  
3) Double-click `run_train.bat` to train.  
4) Double-click `run_realtime.bat` for webcam OR `run_file.bat` for image/video.

> If double-click opens and closes instantly, open **Command Prompt** in this folder and run the `.bat` files there.

### Mac/Linux quick start
```bash
python3 -m venv .venv
# macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Windows CMD: .venv\Scripts\activate.bat
pip install -r requirements.txt
python capture_faces.py        # collect images
python train_recognizer.py     # train
python recognize_realtime.py   # webcam
python recognize_file.py       # image/video
```

---

## 🧪 Capture Tips
- Capture **20–40** images per person (press **C** multiple times).
- Vary angles/expressions/lighting.
- Good light = better accuracy.

## ⚙️ Threshold
In `recognize_realtime.py` and `recognize_file.py`, tweak:
```
CONFIDENCE_THRESHOLD = 70.0
```
Lower → stricter (e.g., 60), higher → more forgiving.

## 📁 Project Structure
```
face_app_complete/
├─ dataset/                 # gets filled after you capture
├─ capture_faces.py
├─ train_recognizer.py
├─ recognize_realtime.py
├─ recognize_file.py
├─ requirements.txt
├─ setup_windows.bat
├─ run_capture.bat
├─ run_train.bat
├─ run_realtime.bat
├─ run_file.bat
└─ README.md
```

## ❓Troubleshooting
- **Cascade not found**: We load from `cv2.data.haarcascades` path — no need to copy XML. If it still errors, ensure OpenCV installed correctly.
- **File not found**: Provide full path or put media file in this folder.
- **Q doesn’t quit**: Click once on the preview window to focus it, then press **Q**. Also try **Esc**.

## 🛡️ Ethics
Get consent, avoid surveillance, delete data on request.
