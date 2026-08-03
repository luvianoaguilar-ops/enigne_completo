#!/usr/bin/env python3
"""Detector de duplicados — pHash de video + escaneo de biblioteca."""
from __future__ import annotations
import argparse, json, cv2, numpy as np
from pathlib import Path
from PIL import Image
import imagehash
from .utils import RESULTS_DIR, guardar_json

def phash_video(ruta, intervalo=1.0, muestras=10):
    cap = cv2.VideoCapture(ruta)
    if not cap.isOpened(): return None
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    salto = max(1, int(fps*intervalo))
    hashes, fn = [], 0
    while len(hashes)<muestras:
        ret, frame = cap.read()
        if not ret: break
        if fn%salto==0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            hashes.append(str(imagehash.phash(Image.fromarray(rgb))))
        fn+=1
    cap.release()
    return ",".join(hashes) if hashes else None

def comparar(h1, h2):
    if not h1 or not h2: return 0.0
    sims = [1-(imagehash.hex_to_hash(a)-imagehash.hex_to_hash(b))/len(a)**2
            for a in h1.split(",") for b in h2.split(",")]
    return round(np.mean(sims)*100, 2)

def escanear(carpeta, ext=".mp4"):
    res = {}
    for v in Path(carpeta).rglob(f"*{ext}"):
        try:
            h = phash_video(str(v))
            if h: res[v.name] = {"ruta":str(v), "phash":h}
        except: pass
    salida = RESULTS_DIR/"biblioteca_phash.json"
    guardar_json(str(salida), res)
    print(f"✅ Biblioteca: {salida}")
    return res

def find_dups(bib_path, umbral=85.0):
    bib = json.load(open(bib_path))
    items = list(bib.items())
    dups = []
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            s = comparar(items[i][1]["phash"], items[j][1]["phash"])
            if s>=umbral: dups.append({"v1":items[i][0],"v2":items[j][0],"sim":s})
    for d in sorted(dups, key=lambda x:x["sim"], reverse=True):
        print(f"🔗 {d['v1']} ↔ {d['v2']} | {d['sim']}%")
    if not dups: print("✅ Sin duplicados")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("scan"); p1.add_argument("--carpeta",default="datasets"); p1.add_argument("--ext",default=".mp4")
    p2 = sub.add_parser("find"); p2.add_argument("--biblioteca",required=True); p2.add_argument("--umbral",type=float,default=85.0)
    args = parser.parse_args()
    if args.cmd=="scan": escanear(args.carpeta, args.ext)
    else: find_dups(args.biblioteca, args.umbral)
