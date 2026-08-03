#!/usr/bin/env python3
"""Limpiador de audio — reducción espectral de ruido."""
from __future__ import annotations
import argparse, librosa, soundfile as sf, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR

def limpiar_ruido(ruta, umbral=0.02):
    ruta = Path(ruta)
    y, sr = librosa.load(str(ruta), sr=22050, mono=True)
    if len(y)==0: raise RuntimeError("Audio vacío")
    stft = librosa.stft(y, n_fft=2048, hop_length=512)
    mag, phase = librosa.magphase(stft)
    ruido = np.percentile(mag, 15, axis=1, keepdims=True)*1.5
    mag_limpio = mag * (mag > ruido)
    y_limpio = librosa.istft(mag_limpio*phase, hop_length=512)
    salida = RESULTS_DIR/f"{ruta.stem}_limpio.wav"
    sf.write(str(salida), y_limpio, sr)
    print(f"✅ Audio limpio: {salida}")
    return {"video":ruta.name, "archivo_limpio":str(salida), "umbral":umbral}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    args = parser.parse_args()
    limpiar_ruido(args.video)
