#!/usr/bin/env python3
"""Movimiento de cámara avanzado — affine estimation + clasificación."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import cv2, numpy as np
from .utils import RESULTS_DIR, guardar_json

def redimensionar(frame, ancho_max=480):
    h, w = frame.shape[:2]
    if w <= ancho_max: return frame
    e = ancho_max/w
    return cv2.resize(frame, (ancho_max, int(h*e)), interpolation=cv2.INTER_AREA)

def clasificar(matriz, desp, validos):
    if matriz is None or len(desp)<8: return {"tipo":"no_confiable","confianza":0.0}
    a, b = matriz[0,0], matriz[0,1]
    escala = math.sqrt(a*a+b*b)
    rot = math.degrees(math.atan2(matriz[1,0], matriz[0,0]))
    dx, dy = np.median(desp, axis=0)
    mag = float(math.sqrt(dx*dx+dy*dy))
    disp = float(np.std(np.linalg.norm(desp-np.median(desp,axis=0), axis=1)))
    if abs(escala-1.0)>0.012: tipo = "zoom_in" if escala>1 else "zoom_out"
    elif abs(rot)>1.5: tipo = "rotacion"
    elif mag<0.6: tipo = "handheld_complejo" if disp>1.8 else "estatica"
    elif abs(dx)>abs(dy)*1.2: tipo = "paneo_derecha" if dx<0 else "paneo_izquierda"
    else: tipo = "tilt_arriba" if dy>0 else "tilt_abajo"
    return {"tipo":tipo, "confianza":min(1.0,len(validos)/80.0), "dx":float(dx),
            "dy":float(dy), "escala":float(escala), "rot":float(rot), "disp":disp}

def agrupar(muestras, intervalo):
    eventos = []
    for m in muestras:
        if not eventos:
            eventos.append({**m, "inicio":m["tiempo"], "fin":m["tiempo"], "_c":1})
            continue
        u = eventos[-1]
        if u["tipo"]==m["tipo"] and m["tiempo"]-u["fin"]<=intervalo*1.8:
            c=u["_c"]; u["fin"]=m["tiempo"]
            u["confianza"]=(u["confianza"]*c+m["confianza"])/(c+1); u["_c"]+=1
        else:
            eventos.append({**m, "inicio":m["tiempo"], "fin":m["tiempo"], "_c":1})
    for e in eventos: e.pop("_c",None)
    return eventos

def analizar_movimiento_camara(ruta_video, intervalo=0.25):
    ruta = Path(ruta_video)
    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened(): raise RuntimeError(f"No se pudo abrir: {ruta}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    salto = max(1, int(round(fps*intervalo)))
    fn, prev, muestras = 0, None, []
    while True:
        ret, frame = cap.read()
        if not ret: break
        if fn%salto: fn+=1; continue
        t = fn/fps
        frame = redimensionar(frame)
        g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev is not None:
            pts = cv2.goodFeaturesToTrack(prev, 180, 0.01, 7)
            if pts is not None:
                nw, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, pts, None)
                if nw is not None and st is not None:
                    v = st.flatten()==1
                    pa, pd = pts[v], nw[v]
                    if len(pa)>=8:
                        mat, _ = cv2.estimateAffinePartial2D(pa, pd, method=cv2.RANSAC)
                        info = clasificar(mat, pd-pa, pa)
                        info["tiempo"] = float(t)
                        muestras.append(info)
        prev = g; fn+=1
    cap.release()
    res = {"video": ruta.name, "intervalo": intervalo, "muestras": muestras,
           "eventos": agrupar(muestras, intervalo)}
    salida = RESULTS_DIR / f"{ruta.stem}_camara.json"
    guardar_json(str(salida), res)
    print(f"✅ Cámara guardada: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--intervalo", type=float, default=0.25)
    args = parser.parse_args()
    analizar_movimiento_camara(args.video, args.intervalo)
