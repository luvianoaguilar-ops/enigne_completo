#!/usr/bin/env python3
import sys, json, cv2, numpy as np
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 CORE/hook_analyzer.py video.mp4")
        return

    cap = cv2.VideoCapture(sys.argv[1])
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    prev = None
    caras = 0
    eventos = []
    i = 0

    while i < fps * 3:
        ok, f = cap.read()
        if not ok:
            break
        small = cv2.resize(f, (240, int(f.shape[0] * 240 / f.shape[1])))
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if len(face.detectMultiScale(g, 1.2, 4)) > 0:
            caras += 1

        if prev is not None:
            diff = float(np.mean(cv2.absdiff(g, prev)))
            if diff > 28:
                eventos.append({"t": round(i / fps, 2), "fuerza": round(diff, 1)})

        prev = g
        i += 1

    cap.release()
    score = min(100, round(40 + (caras / max(1, i)) * 40))
    print(json.dumps({"score_gancho": score, "eventos": eventos}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
