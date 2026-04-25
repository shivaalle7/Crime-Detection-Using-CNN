from ultralytics import YOLO
import cv2
import time

model = YOLO("yolov8n.pt")

crime_labels = ['person', 'handbag', 'backpack']

def detect_crime(frame):
    results = model(frame)

    fight = False
    theft = False
    person_count = 0

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            x1,y1,x2,y2 = map(int, box.xyxy[0])

            if label == "person":
                person_count += 1

            # Fight Detection (multiple persons close)
            if person_count >= 2:
                fight = True

            # Theft Detection
            if label in ['handbag','backpack']:
                theft = True

            color = (0,255,0)

            if fight:
                color = (0,0,255)

            if theft:
                color = (255,0,0)

            cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
            cv2.putText(frame,label,(x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX,0.7,color,2)

    return frame, fight, theft, person_count
