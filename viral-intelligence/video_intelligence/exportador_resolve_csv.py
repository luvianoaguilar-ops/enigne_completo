#!/usr/bin/env python3
"""Exportador CSV para DaVinci Resolve."""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path
from .utils import RESULTS_DIR

def exportar(ruta, reporte, timeline):
    ruta = Path(ruta)
    try:
        dur = reporte["metadatos"]["duracion_segundos"]
        cortes = [float(c["tiempo"]) for c in reporte["visual"]["edicion"]["cortes"]]
    except: return {"error":"Faltan datos"}
    clips = []
    for i,ini in enumerate(cortes):
        fin = cortes[i+1] if i+1<len(cortes) else dur
        notas = timeline["segmentos"][i].get("fase","") if i<len(timeline["segmentos"]) else ""
        clips.append({"nombre":f"Clip_{i+1}","inicio":ini,"fin":fin,"duracion":fin-ini,
                      "ruta":str(ruta),"notas":notas})
    salida = RESULTS_DIR/f"{ruta.stem}_resolve.csv"
    with open(salida,"w",newline="") as f:
        w = csv.writer(f)
        w.writerow(["Clip Name","Start","End","Duration","File Path","Notes"])
        for c in clips:
            w.writerow([c["nombre"],f"{c['inicio']:.3f}",f"{c['fin']:.3f}",
                        f"{c['duracion']:.3f}",c["ruta"],c["notas"]])
    print(f"✅ Resolve CSV: {salida}")
    return salida

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video"); parser.add_argument("--reporte",required=True)
    parser.add_argument("--timeline",required=True)
    args = parser.parse_args()
    exportar(args.video, json.load(open(args.reporte)), json.load(open(args.timeline)))
