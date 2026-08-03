#!/usr/bin/env python3
import sys, json
from pathlib import Path
ZONAS = {"like": {"x": 85, "y": 30, "desc": "iconos derecha"},
         "desc": {"x": 0, "y": 85, "desc": "descripción inferior"}}
def main():
    d = json.loads(Path(sys.argv[1]).read_text())
    prob = []
    for esc in d.get("escenas", []):
        for t in esc.get("textos_ocr", []):
            x, y = t["posicion"][0], t["posicion"][1]
            if x > 800: prob.append({"escena": esc["escena"], "texto": t["texto"], "problema": "choca con likes"})
    print(f"Problemas: {len(prob)}")
    Path("safe_zones.json").write_text(json.dumps(prob, indent=2, ensure_ascii=False))
if __name__ == "__main__": main()
