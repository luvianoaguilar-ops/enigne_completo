#!/usr/bin/env python3
"""Generador de storyboard — JSON + Markdown con tabla de tomas."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import timedelta
from .utils import RESULTS_DIR, guardar_json

def seg_time(s):
    return str(timedelta(seconds=s))

def generar(ruta, reporte, ocr, planos, camara):
    ruta = Path(ruta)
    try:
        dur = reporte["metadatos"]["duracion_segundos"]
        cortes = reporte["visual"]["edicion"]["cortes"]
        bpm = reporte["audio"].get("bpm_estimado",0)
        ritmo = reporte["visual"]["edicion"]["estadisticas_tomas"].get("ritmo","desconocido")
    except:
        return {"error":"Reporte incompleto"}
    ev_cam = camara.get("eventos",[])
    tomas_pl = planos.get("tomas",[])
    tomas = []
    for i,c in enumerate(cortes):
        ini = c["tiempo"]
        fin = cortes[i+1]["tiempo"] if i+1<len(cortes) else dur
        pl = next((p for p in tomas_pl if p["tiempo"]>=ini and p["tiempo"]<=fin), {"plano":"Desconocido"})
        cm = next((e for e in ev_cam if e["inicio"]<=ini and e["fin"]>=ini), {"tipo":"Estática"})
        txt = [t["texto"] for t in ocr.get("segmentos",[]) if ini<=t["inicio"]<=fin or ini<=t["fin"]<=fin]
        beats = len([b for b in reporte.get("audio",{}).get("beats",[]) if ini<=b<=fin])
        tomas.append({"id":i+1,"inicio":ini,"fin":fin,"duracion":fin-ini,
                       "plano":pl.get("plano","?"),"camara":cm.get("tipo","?"),
                       "texto":txt[:3],"beats":beats})
    sb = {"video":ruta.name,"duracion":dur,"bpm":bpm,"ritmo":ritmo,"tomas":tomas}
    salida_j = RESULTS_DIR/f"{ruta.stem}_storyboard.json"
    guardar_json(str(salida_j), sb)
    md = f"# 🎬 Storyboard: {ruta.name}\n**Duración:** {seg_time(dur)} | **BPM:** {bpm:.0f} | **Ritmo:** {ritmo}\n\n"
    md += "| ID | Tiempo | Duración | Plano | Cámara | Beats | Texto |\n|---|---|---|---|---|---|---|\n"
    for t in tomas:
        md += f"| {t['id']} | {seg_time(t['inicio'])}→{seg_time(t['fin'])} | {t['duracion']:.1f}s | {t['plano']} | {t['camara']} | {t['beats']} | {', '.join(t['texto'])} |\n"
    salida_m = RESULTS_DIR/f"{ruta.stem}_storyboard.md"
    with open(salida_m,"w") as f: f.write(md)
    print(f"✅ Storyboard: {salida_j} & {salida_m}")
    return sb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--reporte",required=True); parser.add_argument("--ocr",required=True)
    parser.add_argument("--planos",required=True); parser.add_argument("--camara",required=True)
    args = parser.parse_args()
    generar(args.video, json.load(open(args.reporte)), json.load(open(args.ocr)),
            json.load(open(args.planos)), json.load(open(args.camara)))
