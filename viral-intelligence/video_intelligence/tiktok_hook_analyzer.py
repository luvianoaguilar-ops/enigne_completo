#!/usr/bin/env python3
# Hook score 0-100 - analiza primeros 3 segundos
import sys, json, cv2, numpy as np
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: python3 tiktok_hook_analyzer.py video.mp4"); return
    cap = cv2.VideoCapture(sys.argv[1])
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    prev = None; caras = 0; cortes = 0; i = 0
    while i < int(fps * 3):
        ok, f = cap.read()
        if not ok: break
        g = cv2.cvtColor(cv2.resize(f, (240, int(f.shape[0] * 240 / f.shape[1]))), cv2.COLOR_BGR2GRAY)
        if len(face.detectMultiScale(g, 1.2, 4)) > 0: caras += 1
        if prev is not None and np.mean(cv2.absdiff(g, prev)) > 28: cortes += 1
        prev = g; i += 1
    cap.release()
    score = min(100, int(caras * 3 + cortes * 8 + 20))
    result = {"score": score, "caras_detectadas": caras, "cortes_3s": cortes,
              "calidad": "🔥 VIRAL" if score > 80 else "⚡ BUENO" if score > 60 else "🟡 MEJORABLE"}
    Path("hook_score.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(json.dumps(result, indent=2, ensure_ascii=False))
if __name__ == "__main__": main()
