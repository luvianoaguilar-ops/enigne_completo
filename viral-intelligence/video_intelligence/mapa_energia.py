#!/usr/bin/env python3
"""Mapa de energía audiovisual — audio + visual + movimiento combinados."""
from __future__ import annotations
import argparse, json, subprocess, tempfile
from pathlib import Path
import cv2, librosa, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from .utils import RESULTS_DIR, guardar_json

def normalizar(valores):
    v = np.asarray(valores, dtype=float)
    if len(v) == 0: return v
    mn, mx = np.percentile(v, 5), np.percentile(v, 95)
    if mx - mn < 1e-6: return np.zeros_like(v)
    return np.clip((v - mn) / (mx - mn), 0, 1)

def extraer_audio(video, wav):
    r = subprocess.run(["ffmpeg","-y","-i",str(video),"-vn","-ac","1","-ar","22050","-c:a","pcm_s16le",str(wav)], capture_output=True)
    return r.returncode == 0

def analizar_audio(video):
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp)/"a.wav"
        if not extraer_audio(video, wav): return None
        y, sr = librosa.load(str(wav), sr=22050, mono=True)
        if len(y)==0: return None
        rms = librosa.feature.rms(y=y)[0]
        rms_t = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
        onset = librosa.onset.onset_strength(y=y, sr=sr)
        onset_t = librosa.times_like(onset, sr=sr)
        return {"rms": rms, "rms_t": rms_t, "onset": onset, "onset_t": onset_t}

def analizar_energia(ruta_video, reporte=None, intervalo=0.25):
    ruta = Path(ruta_video)
    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened(): raise RuntimeError(f"No se pudo abrir: {ruta}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    salto = max(1, int(round(fps * intervalo)))
    tiempos, cambios, movimiento = [], [], []
    prev = None; fn = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if fn % salto: fn+=1; continue
        t = fn/fps
        sm = cv2.resize(frame, (320,180))
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        if prev is None: c, m = 0.0, 0.0
        else:
            c = float(cv2.absdiff(prev, g).mean()/255.0)
            pts = cv2.goodFeaturesToTrack(prev, 100, 0.01, 8)
            m = 0.0
            if pts is not None:
                nw, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, pts, None)
                if nw is not None and st is not None:
                    v = st.flatten()==1
                    if np.any(v):
                        m = float(np.mean(np.linalg.norm(nw[v]-pts[v], axis=2)))
        tiempos.append(t); cambios.append(c); movimiento.append(m)
        prev = g; fn+=1
    cap.release()
    tiempos = np.asarray(tiempos)
    cambios = np.asarray(cambios)
    movimiento = np.asarray(movimiento)
    audio = analizar_audio(ruta)
    cortes_raw = (reporte or {}).get("visual",{}).get("edicion",{}).get("cortes",[])
    cortes = np.asarray([float(c["tiempo"]) for c in cortes_raw]) if cortes_raw else np.array([])
    cn, mn = normalizar(cambios), normalizar(movimiento)
    sc = np.array([1.0 if len(cortes) and np.min(np.abs(cortes-t))<=intervalo else 0.0 for t in tiempos])
    if audio:
        ri = np.interp(tiempos, audio["rms_t"], audio["rms"])
        oi = np.interp(tiempos, audio["onset_t"], audio["onset"])
        rn, on = normalizar(ri), normalizar(oi)
        energia = mn*0.25 + cn*0.20 + rn*0.35 + on*0.10 + sc*0.10
    else:
        rn = on = np.zeros(len(tiempos))
        energia = mn*0.45 + cn*0.30 + sc*0.25
    puntos = [{"tiempo": float(t), "energia": float(energia[i]),
               "nivel": "alto" if energia[i]>=0.66 else "medio" if energia[i]>=0.33 else "bajo",
               "movimiento": float(mn[i]), "cambio_visual": float(cn[i]),
               "audio": float(rn[i]), "onset": float(on[i]), "corte": bool(sc[i])}
              for i,t in enumerate(tiempos)]
    res = {"video": ruta.name, "intervalo": intervalo, "audio_disponible": audio is not None,
           "energia_media": float(np.mean(energia)), "energia_maxima": float(np.max(energia)),
           "picos": sorted(puntos, key=lambda x: x["energia"], reverse=True)[:12],
           "puntos": puntos}
    salida_j = RESULTS_DIR / f"{ruta.stem}_energia.json"
    guardar_json(str(salida_j), res)
    plt.figure(figsize=(14,5)); plt.plot(tiempos, energia, color="#7c3aed", lw=2)
    plt.fill_between(tiempos, energia, alpha=0.25, color="#7c3aed")
    plt.ylim(0,1); plt.xlabel("Tiempo (s)"); plt.ylabel("Energía")
    plt.grid(alpha=0.2); plt.tight_layout()
    plt.savefig(RESULTS_DIR/f"{ruta.stem}_energia.png", dpi=160)
    plt.close()
    print(f"✅ Energía guardada: {salida_j}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--reporte", default=None)
    parser.add_argument("--intervalo", type=float, default=0.25)
    args = parser.parse_args()
    rep = json.load(open(args.reporte)) if args.reporte else None
    analizar_energia(args.video, rep, args.intervalo)
