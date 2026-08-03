#!/usr/bin/env python3
"""Loop Seam Detector — detecta punto exacto para loop infinito en TikTok."""
from __future__ import annotations
import argparse, cv2, json, numpy as np
from pathlib import Path

def encontrar_loop(ruta: str, sensibilidad: float = 3.0):
    cap = cv2.VideoCapture(str(ruta))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    
    # Tomar primer frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, first = cap.read()
    first_g = cv2.cvtColor(cv2.resize(first, (160, 90)), cv2.COLOR_BGR2GRAY)
    
    mejores = []
    step = max(1, total // 30)
    for fn in range(total//2, total, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, fn)
        _, f = cap.read()
        if f is None: continue
        f_g = cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY)
        diff = float(np.mean(cv2.absdiff(first_g, f_g)))
        if diff < sensibilidad:
            mejores.append({"frame": fn, "tiempo": round(fn/fps, 2), "diferencia": round(diff, 2)})
    cap.release()
    
    if mejores:
        best = min(mejores, key=lambda x: x["diferencia"])
        print(f"\n🔁 LOOP SEAM DETECTOR\n")
        print(f"  ✅ Loop perfecto en: {best['tiempo']}s (frame {best['frame']})")
        print(f"  📏 Diferencia: {best['diferencia']:.2f} píxeles")
        print(f"  💡 Cortá el video en {best['tiempo']}s para loop infinito en TikTok")
        return best
    else:
        print(f"\n🔁 LOOP SEAM DETECTOR\n  ❌ No se encontró punto de loop (sensibilidad={sensibilidad})")
        print(f"  💡 Probá con --sensibilidad 5.0 para ser menos estricto")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("video"); p.add_argument("--sensibilidad", type=float, default=3.0)
    args = p.parse_args()
    encontrar_loop(args.video, args.sensibilidad)
