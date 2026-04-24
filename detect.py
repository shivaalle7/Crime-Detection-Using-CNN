import cv2
import os
from ultralytics import YOLO
from alerts import save_alert

model = YOLO('yolov8n.pt')
THREAT_CLASSES = ['knife', 'scissors', 'baseball bat']

os.makedirs('snapshots', exist_ok=True)


def run_detection(source):
    cap = cv2.VideoCapture(source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        annotated = results[0].plot()

        names = results[0].names
        boxes = results[0].boxes

        detected = []
        for cls in boxes.cls.tolist() if boxes is not None else []:
            label = names[int(cls)]
            detected.append(label)

        if 'person' in detected and any(x in detected for x in THREAT_CLASSES):
            save_alert(frame, 'Possible armed threat detected')

        cv2.imshow('Crime Detection', annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()