#!/usr/bin/env python3
# Sonido viral score - BPM + energía
import sys, json, subprocess
from pathlib import Path
import librosa, numpy as np
def main():
    if len(sys.argv) < 2: print("Uso: python3 tiktok_sound_viral.py video.mp4"); return
    wav = "_tmp.wav"
    subprocess.run(["ffmpeg", "-y", "-i", sys.argv[1], "-vn", "-ar", "22050", "-ac", "1", wav], capture_output=True)
    y, sr = librosa.load(wav)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])
    rms = librosa.feature.rms(y=y)[0]
    score = 20
    if 110 <= bpm <= 145: score += 40
    if np.mean(rms) > 0.05: score += 20
    result = {"bpm": round(bpm, 1), "energia": round(float(np.mean(rms)), 4), "sound_viral_score": min(100, score)}
    print(json.dumps(result, indent=2))
    Path("sound_score.json").write_text(json.dumps(result, indent=2))
    Path(wav).unlink(missing_ok=True)
if __name__ == "__main__": main()
