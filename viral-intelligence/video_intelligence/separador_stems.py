#!/usr/bin/env python3
"""Separador de stems — HPSS (armónico + percusivo)."""
from __future__ import annotations
import argparse, json, librosa, soundfile as sf, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def separar_audio(ruta):
    ruta = Path(ruta)
    y, sr = librosa.load(str(ruta), sr=22050, mono=True)
    if len(y)==0: raise RuntimeError("Audio vacío")
    harmonic, percussive = librosa.effects.hpss(y)
    base = ruta.stem
    ruta_h = RESULTS_DIR/f"{base}_armonico.wav"
    ruta_p = RESULTS_DIR/f"{base}_percusivo.wav"
    sf.write(str(ruta_h), harmonic, sr)
    sf.write(str(ruta_p), percussive, sr)
    res = {"video":ruta.name, "sr":sr, "duracion":len(y)/sr,
           "armonico":str(ruta_h), "percusivo":str(ruta_p),
           "energia_arm":float(np.mean(np.abs(harmonic))),
           "energia_perc":float(np.mean(np.abs(percussive))),
           "predominio":"Percusivo" if np.mean(np.abs(percussive))>np.mean(np.abs(harmonic)) else "Armónico"}
    salida = RESULTS_DIR/f"{base}_stems.json"
    guardar_json(str(salida), res)
    print(f"✅ Stems guardados: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    args = parser.parse_args()
    separar_audio(args.video)
