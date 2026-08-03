#!/usr/bin/env python3
"""Smart Batch Processor — analiza N videos y genera mega-reporte."""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from datetime import datetime
import sys

def procesar_lote(carpeta: str, n: int = 10):
    videos = sorted(Path(carpeta).glob("*.mp4"))[:n]
    if not videos:
        videos = sorted(Path(carpeta).glob("*.*"))
        videos = [v for v in videos if v.suffix in (".mp4",".mov",".mkv",".webm")][:n]
    print(f"\n📦 BATCH: {len(videos)} videos\n{'='*60}")
    resultados = []
    for i, v in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {v.name}")
        try:
            r = subprocess.run([sys.executable, "run_pipeline.py", str(v), "--tema", v.stem, "--fast"],
                               capture_output=True, text=True, timeout=120, cwd=Path(__file__).parent.parent)
            resultados.append({"video": v.name, "ok": r.returncode==0})
            print(f"  {'✅' if r.returncode==0 else '❌'} Completado")
        except Exception as e:
            resultados.append({"video": v.name, "ok": False, "error": str(e)})
            print(f"  ❌ {e}")

    reporte = {"fecha": datetime.now().isoformat(), "total": len(videos),
               "exitosos": sum(1 for r in resultados if r["ok"]),
               "resultados": resultados}
    out = Path("results/batch_report.json")
    out.write_text(json.dumps(reporte, indent=2, ensure_ascii=False))
    print(f"\n✅ BATCH: {reporte['exitosos']}/{reporte['total']} exitosos")
    return reporte

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("carpeta"); p.add_argument("--n",type=int,default=10)
    args = p.parse_args()
    procesar_lote(args.carpeta, args.n)
