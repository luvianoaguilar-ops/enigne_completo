#!/usr/bin/env python3
import sys, cv2, subprocess
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: auto_crop_vertical.py video.mp4"); return
    cap = cv2.VideoCapture(sys.argv[1])
    W, H = 1080, 1920
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    tmp = "_vert.mp4"
    out = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
    while True:
        ok, f = cap.read()
        if not ok: break
        h, w = f.shape[:2]
        scale = max(W / w, H / h)
        f = cv2.resize(f, (int(w * scale), int(h * scale)))
        y, x = (f.shape[0] - H) // 2, (f.shape[1] - W) // 2
        out.write(f[y:y + H, x:x + W])
    cap.release(); out.release()
    subprocess.run(["ffmpeg", "-y", "-i", tmp, "-c:v", "libx264", "vertical.mp4"], capture_output=True)
    Path(tmp).unlink(missing_ok=True)
    print("✅ vertical.mp4")
if __name__ == "__main__": main()
