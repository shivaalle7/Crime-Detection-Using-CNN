## Crime-Detection-Using-CNN
An advanced real-time surveillance project built using Python, OpenCV, YOLOv8, and Streamlit that detects suspicious criminal activities from CCTV footage or live webcam streams. The system analyzes video frames in real time to identify events such as fight detection, theft detection, and abnormal crowd behavior, then displays alerts through an interactive dashboard.

This project is designed for smart city surveillance, public safety monitoring, offices, malls, banks, parking areas, and restricted zones.

### Project Structure

```text
AI-Crime-Detection-System/
│── app.py                 # Main Streamlit application
│── detector.py            # Fight & theft detection logic using YOLO
│── dashboard.py           # Live analytics dashboard
│── requirements.txt       # Required libraries
│── temp.mp4               # Temporary uploaded video
│── models/
│   └── yolov8n.pt         # YOLO pre-trained model
│── uploads/               # Uploaded CCTV videos
│── evidence/              # Saved suspicious frames
│── screenshots/           # Project screenshots for README
└── README.md
```

### 🔥 Key Features
```
✅ Real-time CCTV / Webcam Monitoring
✅ Fight Detection using Human Activity Analysis
✅ Theft Detection using Object + Person Tracking
✅ YOLOv8 Object Detection
✅ Live Crime Analytics Dashboard
✅ Upload Recorded CCTV Videos
✅ Real-time Alerts & Status Updates
✅ Evidence Frame Monitoring
✅ Streamlit Interactive UI
✅ Scalable for Multiple Cameras
```

### How It Works
```
User selects Live Webcam or Upload CCTV Video
Frames are processed using YOLOv8
System detects:
Persons
Bags / Suspicious objects
Violent interactions
If suspicious activity is found:
Alert displayed instantly
Dashboard updated
Real-time statistics shown in Streamlit panel
```

### Run Locally
```
pip install -r requirements.txt
streamlit run app.py
```
