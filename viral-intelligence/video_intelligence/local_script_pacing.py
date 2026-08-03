#!/usr/bin/env python3
"""Analizador de ritmo de guion (WPM y densidad)."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def analizar_pacing(ruta_guion: str, duracion: float = 30):
    texto = Path(ruta_guion).read_text(encoding="utf-8")
    palabras = len(re.findall(r"\b\w+\b", texto))
    oraciones = len(re.findall(r"[.!?]+", texto))
    wps = palabras/duracion if duracion>0 else 0
    wpm = wps*60
    nivel = "⚡ Muy rápido" if wpm>180 else "✅ Óptimo" if 120<=wpm<=180 else "🐌 Lento" if wpm<90 else "📊 Normal"
    res = {"archivo": Path(ruta_guion).name, "palabras": palabras, "oraciones": oraciones,
           "duracion_estimada": duracion, "wpm": round(wpm,1), "wps": round(wps,2),
           "densidad": round(palabras/(duracion/60)) if duracion>0 else 0, "nivel": nivel}
    salida = RESULTS_DIR / f"{Path(ruta_guion).stem}_pacing.json"
    guardar_json(str(salida), res)
    print(f"✅ Pacing: {wpm:.0f} wpm — {nivel}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("guion")
    parser.add_argument("--duracion", type=float, default=30.0)
    args = parser.parse_args()
    analizar_pacing(args.guion, args.duracion)
