#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINEA TIEMPO v2.0 — Genera timeline CSV + JSON de un video con fases.
Uso: python -m video_intelligence.linea_tiempo --reporte R --ocr O --energia E --camara C
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from .utils import RESULTS_DIR, guardar_json


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def solapa(inicio_a, fin_a, inicio_b, fin_b):
    return inicio_a <= fin_b and fin_a >= inicio_b


def energia_promedio(puntos, inicio, fin):
    valores = [p["energia"] for p in puntos if inicio <= p["tiempo"] <= fin]
    return float(np.mean(valores)) if valores else 0.0


def crear_linea_tiempo(reporte, ocr, energia, camara, nombre_video):
    try:
        duracion = float(reporte["metadatos"]["duracion_segundos"])
    except (KeyError, TypeError):
        duracion = 0.0

    try:
        cortes = [float(c["tiempo"]) for c in reporte["visual"]["edicion"]["cortes"]]
    except (KeyError, TypeError):
        cortes = []

    limites = [0.0]
    for c in sorted(cortes):
        if c > limites[-1] + 0.12:
            limites.append(c)
    if duracion > limites[-1]:
        limites.append(duracion)

    puntos_energia = energia.get("puntos", [])
    segmentos_texto = ocr.get("segmentos", [])
    eventos_camara = camara.get("eventos", [])

    valores_energia = [p["energia"] for p in puntos_energia]
    umbral_pico = float(np.percentile(valores_energia, 85)) if valores_energia else 0.75

    beats = reporte.get("audio", {}).get("beats", [])
    timeline = []

    for i in range(len(limites) - 1):
        inicio = limites[i]
        fin = limites[i + 1]
        energia_media = energia_promedio(puntos_energia, inicio, fin)

        textos = [s["texto"] for s in segmentos_texto
                  if solapa(inicio, fin, s["inicio"], s["fin"])]
        movimientos = [e["tipo"] for e in eventos_camara
                       if solapa(inicio, fin, e["inicio"], e["fin"])]
        beats_seg = len([b for b in beats if inicio <= b <= fin])

        if inicio < 3.0:
            fase = "hook"
        elif fin >= duracion - 2.0:
            fase = "cierre"
        elif energia_media >= umbral_pico:
            fase = "pico_energia"
        else:
            fase = "desarrollo"

        timeline.append({
            "id": i + 1,
            "inicio": round(inicio, 3),
            "fin": round(fin, 3),
            "duracion": round(fin - inicio, 3),
            "fase": fase,
            "energia_media": round(energia_media, 3),
            "beats": beats_seg,
            "texto": textos[:5],
            "camara": list(dict.fromkeys(movimientos))[:4]
        })

    return {"video": nombre_video, "duracion_total": duracion, "segmentos": timeline}


def guardar_timeline(resultado, nombre_base):
    salida_json = RESULTS_DIR / f"{nombre_base}_timeline.json"
    salida_csv = RESULTS_DIR / f"{nombre_base}_timeline.csv"
    guardar_json(str(salida_json), resultado)

    with open(salida_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "inicio", "fin", "duracion", "fase",
            "energia_media", "beats", "texto", "camara"
        ])
        writer.writeheader()
        for s in resultado["segmentos"]:
            row = dict(s)
            row["texto"] = " | ".join(s["texto"])
            row["camara"] = " | ".join(s["camara"])
            writer.writerow(row)

    print(f"✅ Timeline JSON: {salida_json}")
    print(f"✅ Timeline CSV: {salida_csv}")
    return salida_json, salida_csv


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reporte", required=True)
    parser.add_argument("--ocr", required=True)
    parser.add_argument("--energia", required=True)
    parser.add_argument("--camara", required=True)
    args = parser.parse_args()

    reporte = cargar_json(args.reporte)
    ocr = cargar_json(args.ocr)
    energia = cargar_json(args.energia)
    camara = cargar_json(args.camara)
    nombre_base = Path(args.reporte).stem.replace("_analisis", "")
    resultado = crear_linea_tiempo(reporte, ocr, energia, camara, nombre_base)
    guardar_timeline(resultado, nombre_base)
