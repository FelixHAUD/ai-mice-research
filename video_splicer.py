# pip install opencv-python

import cv2
import os
import sys

# Using this time check progress of video splice
import time
from tqdm import tqdm 

# Input/output paths
input_dir   = ".\\mice-videos"  
output_root  = ".\\mice-videos\\quadrants"
os.makedirs(output_root, exist_ok=True)

# Error check for input/output paths
if not os.path.exists(input_dir):
    print(f"Input directory does not exist: {input_dir}")
    sys.exit(1)
if not os.path.exists(output_root):
    print(f"Output directory does not exist: {output_root}")
    sys.exit(1)

video_files = [
    f for f in os.listdir(input_dir)
    if os.path.isfile(os.path.join(input_dir, f)) and f.lower().endswith(".mp4")
]

if not video_files:
    print(f"No MP4s found in {input_dir}")
    sys.exit(1)
for vid in video_files:
    input_path = os.path.join(input_dir, vid)
    stem, _ = os.path.splitext(vid)
    output_dir = os.path.join(output_root, stem)
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w2 = w // 2
    h2 = h // 2

    # set up writers
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writers = {
        "top_left":     cv2.VideoWriter(os.path.join(output_dir, "top_left.mp4"),     fourcc, fps, (w2, h2)),
        "top_right":    cv2.VideoWriter(os.path.join(output_dir, "top_right.mp4"),    fourcc, fps, (w2, h2)),
        "bottom_left":  cv2.VideoWriter(os.path.join(output_dir, "bottom_left.mp4"),  fourcc, fps, (w2, h2)),
        "bottom_right": cv2.VideoWriter(os.path.join(output_dir, "bottom_right.mp4"), fourcc, fps, (w2, h2)),
    }

    print(f"\nProcessing {vid} ({total} frames)…")
    start = time.time()

    # you can replace tqdm(...) with range(total) if you don't have tqdm installed
    for _ in tqdm(range(total), desc=stem):
        ret, frame = cap.read()
        if not ret:
            break

        # crop quadrants
        writers["top_left"].write(frame[0:h2, 0:w2])
        writers["top_right"].write(frame[0:h2, w2:w])
        writers["bottom_left"].write(frame[h2:h, 0:w2])
        writers["bottom_right"].write(frame[h2:h, w2:w])

    cap.release()
    for w in writers.values():
        w.release()

    elapsed = time.time() - start
    print(f"Done in {elapsed:.1f}s. Outputs in: {output_dir}")