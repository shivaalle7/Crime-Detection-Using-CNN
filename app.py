import streamlit as st
import tempfile
import os
import cv2
import pandas as pd
from datetime import datetime
from ultralytics import YOLO


APP_TITLE = "Crime AI Surveillance Dashboard"
MODEL_PATH = "yolov8n.pt"
CONFIDENCE = 0.45

# COCO suspicious classes available in pretrained model
THREAT_CLASSES = [
    "knife",          # if custom model used
    "scissors",
    "baseball bat",
    "bottle",
    "person"
]

LOG_DIR = "logs"
SNAP_DIR = "snapshots"
LOG_FILE = os.path.join(LOG_DIR, "alerts.csv")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(SNAP_DIR, exist_ok=True)

# =====================================================
# LOAD MODEL
# =====================================================
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# =====================================================
# UI SETTINGS
# =====================================================
st.set_page_config(
    page_title=APP_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM CSS
# =====================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg,#0f172a,#111827);
    color: white;
}
[data-testid="stSidebar"] {
    background: #0b1220;
}
.block-container {
    padding-top: 1rem;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 16px;
}
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNCTIONS
# =====================================================
def save_alert(frame, message):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    img_path = os.path.join(SNAP_DIR, f"{now}.jpg")

    cv2.imwrite(img_path, frame)

    row = {
        "time": now,
        "message": message,
        "image": img_path
    }

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(LOG_FILE, index=False)


def detect_frame(frame):
    results = model(frame, conf=CONFIDENCE)

    boxes = results[0].boxes
    names = results[0].names

    detected = []

    if boxes is not None:
        for cls in boxes.cls.tolist():
            label = names[int(cls)]
            detected.append(label)

    annotated = results[0].plot()

    # Crime Logic
    if "person" in detected and (
        "scissors" in detected or
        "baseball bat" in detected or
        "knife" in detected
    ):
        save_alert(frame, "Possible armed threat detected")

    return annotated, detected


def run_webcam():
    stframe = st.empty()
    cap = cv2.VideoCapture(0)

    stop_btn = st.button("Stop Camera")

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            st.error("Unable to access webcam")
            break

        annotated, detected = detect_frame(frame)

        stframe.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_container_width=True
        )

        if stop_btn:
            break

    cap.release()


def run_uploaded_video(video_path):
    stframe = st.empty()
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        annotated, detected = detect_frame(frame)

        stframe.image(
            cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
            channels="RGB",
            use_container_width=True
        )

    cap.release()

# =====================================================
# HEADER
# =====================================================
st.title("🛡 Crime AI Surveillance Dashboard")
st.caption("Real-time smart CCTV monitoring using YOLO + Streamlit")

# =====================================================
# DASHBOARD METRICS
# =====================================================
col1, col2, col3 = st.columns(3)

total_alerts = 0
if os.path.exists(LOG_FILE):
    total_alerts = len(pd.read_csv(LOG_FILE))

col1.metric("Active Cameras", "03")
col2.metric("Today Alerts", total_alerts)
col3.metric("System Health", "99%")

# =====================================================
# SIDEBAR MENU
# =====================================================
mode = st.sidebar.radio(
    "Select Mode",
    [
        "Live Webcam",
        "Upload CCTV Video",
        "Admin Dashboard"
    ]
)

# =====================================================
# LIVE WEBCAM
# =====================================================
if mode == "Live Webcam":
    st.subheader("📷 Live Monitoring")

    if st.button("Start Webcam Detection"):
        run_webcam()

# =====================================================
# VIDEO UPLOAD
# =====================================================
elif mode == "Upload CCTV Video":
    st.subheader("🎥 Upload CCTV Footage")

    uploaded = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded:
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(uploaded.read())

        st.video(temp.name)

        if st.button("Analyze Video"):
            run_uploaded_video(temp.name)
            st.success("Video analysis completed")

# =====================================================
# ADMIN DASHBOARD
# =====================================================
elif mode == "Admin Dashboard":
    st.subheader("📊 Alert Logs Dashboard")

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download CSV Report",
            df.to_csv(index=False),
            file_name="crime_alerts.csv",
            mime="text/csv"
        )
    else:
        st.info("No alerts found yet.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("Developed for Final Year Major Project | AI Surveillance System")