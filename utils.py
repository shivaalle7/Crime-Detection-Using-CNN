import os

def ensure_dirs():
    os.makedirs('logs', exist_ok=True)
    os.makedirs('snapshots', exist_ok=True)