#!/usr/bin/env python3
"""Auto-Chapter Marker — detecta y marca capítulos automáticamente."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

def detectar_capitulos(video: str, sensibilidad: float = 0.30):
    cmd = ["ffmpeg", "-i", video, "-vf", f"select='gt(scene,{sensibilidad})',showinfo",
           "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    import re
    tiempos = re.findall(r"pts_time:([\d.]+)", r.stderr)
    capitulos = []
    for i, t in enumerate(sorted(set(float(x) for x in tiempos))):
        capitulos.append({"capitulo": i+1, "tiempo": round(t, 1),
                          "etiqueta": f"Capítulo {i+1}"})
    return capitulos

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("video"); p.add_argument("--sensibilidad",type=float,default=0.30)
    args = p.parse_args()
    caps = detectar_capitulos(args.video, args.sensibilidad)
    out = f"results/{Path(args.video).stem}_chapters.json"
    Path(out).write_text(json.dumps({"video": Path(args.video).name, "capitulos": caps}, indent=2))
    print(f"✅ {len(caps)} capítulos detectados: {out}")
    for c in caps: print(f"  {c['capitulo']:2d}. {c['tiempo']:6.1f}s — {c['etiqueta']}")
