#!/usr/bin/env python3
"""Control de continuidad entre tomas con YOLOv8."""
from __future__ import annotations
import argparse, json, cv2, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def comparar(f1, f2, clases=None):
    if clases is None: clases = [0]  # persona
    try:
        from ultralytics import YOLO
        modelo = YOLO("yolov8n.pt")
    except ImportError:
        return [{"tipo":"error", "obj":"Instala: pip install ultralytics"}]
    r1 = modelo(f1, verbose=False)
    r2 = modelo(f2, verbose=False)
    o1 = [{"cls":int(b.cls),"xyxy":b.xyxy[0].tolist()} for r in r1 for b in r.boxes if int(b.cls) in clases]
    o2 = [{"cls":int(b.cls),"xyxy":b.xyxy[0].tolist()} for r in r2 for b in r.boxes if int(b.cls) in clases]
    diffs = []
    for a in o1:
        match = next((b for b in o2 if b["cls"]==a["cls"]), None)
        if not match:
            diffs.append({"tipo":"desaparicion","obj":modelo.names[a["cls"]]})
            continue
        c1 = [(a["xyxy"][0]+a["xyxy"][2])/2, (a["xyxy"][1]+a["xyxy"][3])/2]
        c2 = [(match["xyxy"][0]+match["xyxy"][2])/2, (match["xyxy"][1]+match["xyxy"][3])/2]
        d = np.linalg.norm(np.array(c1)-np.array(c2))
        if d>0.3: diffs.append({"tipo":"desplazamiento","obj":modelo.names[a["cls"]],"dist":float(d)})
    for b in o2:
        if not any(a["cls"]==b["cls"] for a in o1):
            diffs.append({"tipo":"aparicion","obj":modelo.names[b["cls"]]})
    return diffs

def analizar(ruta, reporte):
    cap = cv2.VideoCapture(ruta)
    if not cap.isOpened(): raise RuntimeError("No se pudo abrir")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    try:
        cortes = [float(c["tiempo"]) for c in reporte["visual"]["edicion"]["cortes"]]
    except:
        cortes = list(np.arange(0, cap.get(cv2.CAP_PROP_FRAME_COUNT)/fps, 5.0))
    probs = []
    for i in range(len(cortes)-1):
        t1, t2 = cortes[i], cortes[i+1]
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t1*fps))
        ret1, f1 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t2*fps)-1)
        ret2, f2 = cap.read()
        if not (ret1 and ret2): continue
        d = comparar(cv2.resize(f1,(640,360)), cv2.resize(f2,(640,360)))
        if d: probs.append({"toma_inicio":i+1,"toma_fin":i+2,"tiempo":round(t1,2),"diferencias":d})
    cap.release()
    res = {"video":Path(ruta).name, "total":len(probs), "problemas":probs}
    salida = RESULTS_DIR/f"{Path(ruta).stem}_continuidad.json"
    guardar_json(str(salida), res)
    print(f"✅ Continuidad: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--reporte", required=True)
    args = parser.parse_args()
    analizar(args.video, json.load(open(args.reporte)))
