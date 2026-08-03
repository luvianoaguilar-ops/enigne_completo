#!/usr/bin/env python3
import sys, json
from pathlib import Path
def main():
    d = json.loads(Path(sys.argv[1]).read_text())
    print(f"RECETA: {d['metadata']['duracion_segundos']}s, {len(d['escenas'])} planos, {d.get('estadisticas',{}).get('cortes_por_minuto')} cpm, {d['audio'].get('bpm')} bpm")
    Path("recipe.txt").write_text(json.dumps(d["estadisticas"], indent=2))
if __name__ == "__main__": main()
