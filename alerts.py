import cv2
import os
import pandas as pd
from datetime import datetime

os.makedirs('logs', exist_ok=True)
os.makedirs('snapshots', exist_ok=True)
LOG_FILE = 'logs/alerts.csv'


def save_alert(frame, message):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    img_path = f'snapshots/{now}.jpg'
    cv2.imwrite(img_path, frame)

    row = {'time': now, 'message': message, 'image': img_path}

    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    else:
        df = pd.DataFrame([row])

    df.to_csv(LOG_FILE, index=False)