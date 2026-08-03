#!/usr/bin/env python3
# Optimizador formato TikTok
import sys, json
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: python3 tiktok_format_optimizer.py adn_video.json"); return
    d = json.loads(Path(sys.argv[1]).read_text())
    m = d["metadata"]
    e = d.get("estadisticas", {})
    tips = []
    dur = m["duracion_segundos"]
    if not 7 <= dur <= 60: tips.append(f"⚠️ Duración {dur}s - ideal 7-34s")
    else: tips.append(f"✅ Duración {dur}s óptima")
    if e.get("cortes_por_minuto", 0) < 14: tips.append("⚠️ Pocos cortes, subí a 14+ cpm")
    if "1080x1920" not in m["resolucion"]: tips.append("⚠️ No es vertical 9:16")
    print("\n".join(tips))
    Path("format_report.json").write_text(json.dumps({"tips": tips}, indent=2))
if __name__ == "__main__": main()
