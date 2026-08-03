#!/usr/bin/env python3
"""Multi-Format Export — exporta en 9:16, 16:9, 1:1 simultáneamente."""
from __future__ import annotations
import argparse, subprocess, json
from pathlib import Path

FORMATS = {
    "tiktok": {"aspect": "9:16", "size": "1080x1920", "vf": "crop=ih*9/16:ih,scale=1080:1920"},
    "youtube": {"aspect": "16:9", "size": "1920x1080", "vf": "crop=iw:iw*9/16,scale=1920:1080"},
    "cuadrado": {"aspect": "1:1", "size": "1080x1080", "vf": "crop=min(iw\\,ih):min(iw\\,ih),scale=1080:1080"},
    "vertical_4_5": {"aspect": "4:5", "size": "1080x1350", "vf": "crop=ih*4/5:ih,scale=1080:1350"},
}

def exportar(video: str, formatos: list = None):
    src = Path(video); base = src.stem
    if formatos is None: formatos = list(FORMATS.keys())
    resultados = {}
    for fmt in formatos:
        if fmt not in FORMATS: continue
        cfg = FORMATS[fmt]
        out = f"results/{base}_{fmt}.mp4"
        cmd = ["ffmpeg", "-y", "-i", str(src), "-vf", cfg["vf"], "-c:v", "libx264",
               "-preset", "fast", "-c:a", "aac", out]
        r = subprocess.run(cmd, capture_output=True)
        ok = r.returncode == 0
        resultados[fmt] = {"archivo": out, "formato": cfg["aspect"], "size": cfg["size"], "ok": ok}
        print(f"  {'✅' if ok else '❌'} {fmt:12} → {cfg['aspect']:5} {cfg['size']:11} → {out}")
    Path(f"results/{base}_exports.json").write_text(json.dumps(resultados, indent=2))
    return resultados

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("video")
    p.add_argument("--formatos", nargs="+", choices=list(FORMATS.keys()), default=list(FORMATS.keys()))
    args = p.parse_args()
    print(f"\n📦 Exportando {Path(args.video).name} en {len(args.formatos)} formatos...\n")
    exportar(args.video, args.formatos)
