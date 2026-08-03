#!/usr/bin/env python3
"""Analyzer V2 — Motor principal de análisis técnico de video."""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any
import cv2
import librosa
import numpy as np

from .utils import RESULTS_DIR, guardar_json


def ejecutar(comando):
    r = subprocess.run(comando, capture_output=True, text=True, check=False)
    if r.returncode != 0:
        raise RuntimeError(f"Error: {' '.join(comando)}\n{r.stderr}")
    return r.stdout


def vf(v, d=0.0):
    try:
        return float(v)
    except (ValueError, TypeError):
        return d


def parse_fps(v):
    if not v or v == "0/0":
        return 0.0
    if "/" in v:
        n, d = v.split("/", 1)
        return float(n) / float(d) if float(d or 1) else 0.0
    return float(v)


def ffprobe(ruta):
    s = ejecutar(["ffprobe", "-v", "error", "-show_format", "-show_streams",
                   "-of", "json", str(ruta)])
    d = json.loads(s)
    vs = next((x for x in d.get("streams", []) if x.get("codec_type") == "video"), {})
    as_ = next((x for x in d.get("streams", []) if x.get("codec_type") == "audio"), {})
    fmt = d.get("format", {})
    w, h = int(vs.get("width", 0) or 0), int(vs.get("height", 0) or 0)
    fps = parse_fps(vs.get("avg_frame_rate") or vs.get("r_frame_rate"))
    return {
        "archivo": Path(ruta).name,
        "duracion_segundos": vf(fmt.get("duration")),
        "video": {
            "codec": vs.get("codec_name"),
            "ancho": w, "alto": h,
            "orientacion": "vertical" if h > w else "horizontal" if w > h else "cuadrado",
            "fps": fps,
        },
        "audio": {
            "presente": bool(as_),
            "codec": as_.get("codec_name"),
            "sample_rate": int(as_.get("sample_rate", 0) or 0),
        },
    }


def analizar_visual(ruta, mps=4.0, umbral=0.55):
    cap = cv2.VideoCapture(str(ruta))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    salto = max(1, int(fps / mps))
    br, co, sa, ni, mov, dif, cortes = [], [], [], [], [], [], []
    prev, prev_g = None, None
    last_cut = -10.0
    fn = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if fn % salto:
            fn += 1
            continue
        t = fn / fps
        sm = cv2.resize(frame, (320, 180))
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        br.append(float(np.mean(g)))
        co.append(float(np.std(g)))
        sa.append(float(np.mean(hsv[:, :, 1])))
        ni.append(float(cv2.Laplacian(g, cv2.CV_64F).var()))

        if prev is not None:
            ha = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY) if len(prev.shape) == 3 else prev
            hb = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY) if len(sm.shape) == 3 else sm
            h1 = cv2.calcHist([cv2.cvtColor(prev, cv2.COLOR_BGR2HSV)], [0, 1], None, [32, 32], [0, 180, 0, 256])
            h2 = cv2.calcHist([cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)], [0, 1], None, [32, 32], [0, 180, 0, 256])
            cv2.normalize(h1, h1)
            cv2.normalize(h2, h2)
            diff = 1.0 - cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
            dif.append(diff)

            pts = cv2.goodFeaturesToTrack(prev_g, 150, 0.01, 8)
            mm = 0.0
            if pts is not None:
                nw, st, _ = cv2.calcOpticalFlowPyrLK(prev_g, g, pts, None)
                if nw is not None and st is not None:
                    v = st.flatten() == 1
                    if np.any(v):
                        mm = float(np.mean(np.linalg.norm(nw[v] - pts[v], axis=2)))
            mov.append(mm)

            if diff >= umbral and t - last_cut >= 0.35:
                cortes.append({
                    "frame": fn, "tiempo": t,
                    "confianza": min(1.0, diff),
                    "tipo": "fuerte" if diff >= 0.8 else "suave",
                })
                last_cut = t

        prev = sm
        prev_g = g
        fn += 1
    cap.release()

    mm = float(np.mean(mov)) if mov else 0
    if mm < 0.8:
        cam = "estática"
    elif mm < 2.5:
        cam = "suave"
    elif mm < 6:
        cam = "handheld"
    else:
        cam = "intensa"

    nit = float(np.mean(ni)) if ni else 0
    durs = []
    ts = [0.0] + [c["tiempo"] for c in cortes]
    for i in range(len(ts) - 1):
        if ts[i + 1] > ts[i]:
            durs.append(ts[i + 1] - ts[i])
    md = float(np.mean(durs)) if durs else 0
    ritmo = "muy rápido" if md < 1.2 else "rápido" if md < 2.5 else "medio" if md < 5 else "lento"

    return {
        "imagen": {
            "brillo_medio": float(np.mean(br)) if br else 0,
            "contraste_medio": float(np.mean(co)) if co else 0,
            "saturacion_media": float(np.mean(sa)) if sa else 0,
            "nitidez_media": nit,
            "posible_desenfoque": nit < 60,
        },
        "movimiento": {
            "intensidad_media": mm,
            "tipo_estimado": cam,
        },
        "edicion": {
            "total_cortes": len(cortes),
            "cortes": cortes,
            "estadisticas_tomas": {
                "cantidad_tomas": len(durs),
                "duracion_media": md,
                "ritmo": ritmo,
            },
        },
    }


def analizar_audio_local(ruta):
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        try:
            ejecutar(["ffmpeg", "-y", "-i", str(ruta), "-vn", "-ac", "1",
                      "-ar", "22050", "-c:a", "pcm_s16le", str(wav)])
        except RuntimeError:
            return {"presente": False}
        y, sr = librosa.load(str(wav), sr=22050, mono=True)
        if len(y) == 0:
            return {"presente": False}
        tempo, bf = librosa.beat.beat_track(y=y, sr=sr)
        beats = librosa.frames_to_time(bf, sr=sr)
        rms = librosa.feature.rms(y=y)[0]
        return {
            "presente": True,
            "duracion": float(librosa.get_duration(y=y, sr=sr)),
            "bpm_estimado": float(np.asarray(tempo).reshape(-1)[0]),
            "energia_media": float(np.mean(rms)),
            "beats": beats[:500].tolist(),
        }


def sincronia(cortes, beats, tol=0.15):
    tc = [float(c["tiempo"]) for c in cortes]
    ba = np.asarray(beats)
    if not tc or len(ba) == 0:
        return {"porcentaje": 0, "cortes_sincronizados": 0, "total_cortes": len(tc)}
    sync = sum(1 for c in tc if float(np.min(np.abs(ba - c))) <= tol)
    return {
        "porcentaje": sync / len(tc) if tc else 0,
        "cortes_sincronizados": sync,
        "total_cortes": len(tc),
    }


def hook(ruta, dur=3.0):
    cap = cv2.VideoCapture(str(ruta))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    lim = int(fps * dur)
    cams, nis, sas = [], [], []
    prev = None
    for _ in range(lim):
        ok, f = cap.read()
        if not ok:
            break
        sm = cv2.resize(f, (320, 180))
        g = cv2.cvtColor(sm, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(sm, cv2.COLOR_BGR2HSV)
        nis.append(float(cv2.Laplacian(g, cv2.CV_64F).var()))
        sas.append(float(np.mean(hsv[:, :, 1])))
        if prev is not None:
            cams.append(float(cv2.absdiff(prev, g).mean()))
        prev = g
    cap.release()
    c = float(np.mean(cams)) if cams else 0
    n = float(np.mean(nis)) if nis else 0
    s = float(np.mean(sas)) if sas else 0
    sc = min(1.0, c / 20) * 0.45 + min(1.0, n / 500) * 0.25 + min(1.0, s / 150) * 0.30
    return {
        "score_visual_hook": sc,
        "nota": "Hook fuerte" if sc >= 0.65 else "Hook medio" if sc >= 0.4 else "Hook débil",
    }


def receta(meta, vis, au, hk, syn):
    tomas = vis["edicion"]["estadisticas_tomas"]
    mov = vis["movimiento"]
    img = vis["imagen"]
    return {
        "formato": meta["video"]["orientacion"],
        "ritmo_edicion": tomas.get("ritmo"),
        "duracion_media_toma": tomas.get("duracion_media"),
        "movimiento_camara": mov["tipo_estimado"],
        "bpm_referencia": au.get("bpm_estimado", 0),
        "sincronia_musical": syn["porcentaje"],
        "hook": {"score": hk["score_visual_hook"], "evaluacion": hk["nota"]},
        "look": {
            "brillo": img["brillo_medio"],
            "contraste": img["contraste_medio"],
            "saturacion": img["saturacion_media"],
            "nitidez": img["nitidez_media"],
        },
    }


def analizar_video(ruta_video: str):
    ruta = Path(ruta_video).expanduser().resolve()
    if not ruta.exists():
        raise FileNotFoundError(f"No existe: {ruta}")
    print("  → ffprobe...")
    meta = ffprobe(ruta)
    print("  → visual...")
    vis = analizar_visual(ruta)
    print("  → audio...")
    au = analizar_audio_local(ruta)
    print("  → hook...")
    hk = hook(ruta)
    syn = sincronia(vis["edicion"]["cortes"], au.get("beats", []))
    rep = receta(meta, vis, au, hk, syn)
    reporte = {
        "metadatos": meta, "visual": vis, "audio": au,
        "hook": hk, "sincronia": syn, "receta": rep,
    }
    salida = RESULTS_DIR / f"{ruta.stem}_analisis.json"
    guardar_json(str(salida), reporte)
    print(f"  ✅ {salida}")
    return reporte


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    args = parser.parse_args()
    analizar_video(args.video)
