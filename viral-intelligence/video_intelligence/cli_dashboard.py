#!/usr/bin/env python3
import json
from pathlib import Path
def main():
    print("=" * 60 + "\n🧬 ADN LIBRARY DASHBOARD\n" + "=" * 60)
    for f in sorted(Path("dataset").glob("*/adn_video.json"))[-20:]:
        d = json.loads(f.read_text())
        print(f"{f.parent.name[:20]:20} | {d['metadata']['duracion_segundos']:5.1f}s | cpm {d.get('estadisticas',{}).get('cortes_por_minuto',0):4.1f} | {d['audio'].get('bpm',0):5.1f} bpm")
if __name__ == "__main__": main()
