#!/usr/bin/env python3
# Curva de retención estimada
import sys, json, numpy as np
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: python3 tiktok_retention_curve.py adn_video.json"); return
    d = json.loads(Path(sys.argv[1]).read_text())
    dur = d["metadata"]["duracion_segundos"]
    t = np.linspace(0, dur, int(dur * 2))
    r = np.ones(len(t)) * 95
    for i, sec in enumerate(t):
        if sec < 3 and d["escenas"][0]["duracion_seg"] > 2: r[i] -= 3
    result = {"duracion": dur, "ret_promedio": round(float(np.mean(r)), 1),
              "curva": [{"t": round(float(x), 1), "r": round(float(y), 1)} for x, y in zip(t, r)]}
    Path("retention_curve.json").write_text(json.dumps(result, indent=2))
    print(f"Retención promedio: {result['ret_promedio']}%")
if __name__ == "__main__": main()
