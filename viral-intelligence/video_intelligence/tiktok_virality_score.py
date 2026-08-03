#!/usr/bin/env python3
# Score final combinado
import sys, json
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: python3 tiktok_virality_score.py adn_video.json [hook_score.json] [sound_score.json]"); return
    adn = json.loads(Path(sys.argv[1]).read_text())
    hook = 50; sound = 50
    if len(sys.argv) > 2 and Path(sys.argv[2]).exists(): hook = json.loads(Path(sys.argv[2]).read_text()).get("score", 50)
    if len(sys.argv) > 3 and Path(sys.argv[3]).exists(): sound = json.loads(Path(sys.argv[3]).read_text()).get("sound_viral_score", 50)
    base = adn.get("estadisticas", {}).get("cortes_por_minuto", 15) / 30 * 20
    final = min(100, int(hook * 0.4 + sound * 0.3 + base + 20))
    print(f"🎯 VIRALITY FINAL: {final}/100")
    Path("virality_final.json").write_text(json.dumps({"score": final}, indent=2))
if __name__ == "__main__": main()
