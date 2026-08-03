#!/usr/bin/env python3
"""Mapas de saliencia visual con StaticSaliencySpectralResidual."""
from __future__ import annotations
import argparse, json, cv2, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def generar_saliencia(ruta, intervalo=2.0):
    ruta = Path(ruta)
    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened(): raise RuntimeError("No se pudo abrir")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    salto = max(1, int(fps*intervalo))
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    analisis, fn = [], 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if fn%salto: fn+=1; continue
        t = fn/fps
        sm = cv2.resize(frame, (480,270))
        ok, mapa = saliency.computeSaliency(sm)
        if ok:
            _, max_val, _, max_loc = cv2.minMaxLoc((mapa*255).astype("uint8"))
            analisis.append({"tiempo":round(t,2), "frame":fn,
                             "punto_max":{"x":max_loc[0],"y":max_loc[1]},
                             "concentracion":float(np.mean(mapa))})
        fn+=1
    cap.release()
    res = {"video":ruta.name, "intervalo":intervalo, "muestras":analisis}
    salida = RESULTS_DIR/f"{ruta.stem}_saliency.json"
    guardar_json(str(salida), res)
    print(f"✅ Saliencia guardada: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--intervalo", type=float, default=2.0)
    args = parser.parse_args()
    generar_saliencia(args.video, args.intervalo)
