#!/usr/bin/env python3
"""Detector de subtítulos — legibilidad, WPM, zona segura."""
from __future__ import annotations
import argparse, json, re, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def legibilidad(seg, w, h):
    tam = seg["ancho"]*seg["alto"]*100
    cx, cy = seg["x"]+seg["ancho"]/2, seg["y"]+seg["alto"]/2
    dist = min(cx, 1-cx, cy, 1-cy)
    st = min(1.0, tam/2.0)
    sp = min(1.0, dist*5)
    sc = st*0.6 + sp*0.4
    return {"score":round(sc,2), "tam":round(tam,2), "dist":round(dist,2),
            "nota":"Excelente" if sc>0.8 else "Buena" if sc>0.6 else "Regular" if sc>0.4 else "Mala"}

def analizar_subtitulos(ruta, ocr_data=None, reporte=None):
    ruta = Path(ruta)
    if ocr_data is None:
        from .texto_ocr import analizar_texto_video
        ocr_data = analizar_texto_video(str(ruta), intervalo=0.3)
    if not ocr_data.get("disponible"):
        return {"error":"OCR no disponible", "subtitulos":[]}
    try:
        w, h = reporte["metadatos"]["video"]["ancho"], reporte["metadatos"]["video"]["alto"]
    except:
        w, h = 1920, 1080
    subs = []
    for s in ocr_data.get("segmentos",[]):
        palabras = len(re.findall(r'\b\w+\b', s["texto"]))
        dur = s["fin"]-s["inicio"]
        wpm = (palabras/dur)*60 if dur>0 else 0
        leg = legibilidad(s, w, h)
        problemas = []
        if wpm > 200: problemas.append("Velocidad alta")
        if palabras > 12: problemas.append("Demasiado largo")
        if leg["score"] < 0.6: problemas.append(leg["nota"])
        subs.append({**s, "palabras":palabras, "wpm":round(wpm,1), "legibilidad":leg,
                     "es_sub":dur<=5 and palabras<=15, "problemas":problemas})
    validos = [s for s in subs if s["es_sub"]]
    res = {"video":ruta.name, "total_texto":len(subs), "total_subs":len(validos),
           "wpm_prom":round(np.mean([s["wpm"] for s in validos]),1) if validos else 0,
           "leg_prom":round(np.mean([s["legibilidad"]["score"] for s in validos]),2) if validos else 0,
           "subtitulos": validos}
    salida = RESULTS_DIR / f"{ruta.stem}_subtitulos.json"
    guardar_json(str(salida), res)
    print(f"✅ Subtítulos guardados: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--reporte", default=None)
    args = parser.parse_args()
    rep = json.load(open(args.reporte)) if args.reporte else None
    analizar_subtitulos(args.video, reporte=rep)
