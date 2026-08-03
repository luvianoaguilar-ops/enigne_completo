#!/usr/bin/env python3
import sys, json
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 CORE/viral_score.py dataset/ID/adn_video.json")
        return

    d = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    e, m, a = d.get("estadisticas", {}), d.get("metadata", {}), d.get("audio", {})

    s = 0
    dur = m.get("duracion_segundos", 60)

    if 7 <= dur <= 34:
        s += 20

    cpm = e.get("cortes_por_minuto", 0)
    if cpm >= 14:
        s += 20

    esc = d.get("escenas", [])
    if esc and esc[0]["duracion_seg"] <= 1.6:
        s += 20

    bpm = a.get("bpm", 0)
    if 110 <= bpm <= 145:
        s += 20

    s = min(100, s + 20)
    print(f"VIRAL SCORE: {s}/100")


if __name__ == "__main__":
    main()
