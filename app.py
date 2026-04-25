# app.py

import streamlit as st
import cv2
import time
from detector import detect_crime

st.set_page_config(
    page_title="🚨 Smart Crime Detection",
    layout="wide"
)

st.title("🚨 AI Crime Surveillance Dashboard")

menu = st.sidebar.selectbox(
    "Select Source",
    ["Live Webcam", "Upload CCTV Video"]
)

col1, col2 = st.columns([3,1])

frame_area = col1.empty()
stats = col2.empty()

run = st.button("▶ Start Detection")

cap = None

if menu == "Live Webcam":
    cap = cv2.VideoCapture(0)

elif menu == "Upload CCTV Video":
    file = st.file_uploader("Upload Video")

    if file:
        with open("temp.mp4", "wb") as f:
            f.write(file.read())

        cap = cv2.VideoCapture("temp.mp4")

if run and cap is not None:

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        frame, fight, theft, count = detect_crime(frame)

        frame_area.image(frame, channels="BGR")

        status = "Safe"

        if fight:
            status = "⚠ Fight Detected"

        if theft:
            status = "🚨 Theft Detected"

        stats.markdown(f"""
        ## 📊 Live Stats

        **People Count:** {count}

        **Status:** {status}

        **Time:** {time.strftime('%H:%M:%S')}
        """)

    cap.release()
