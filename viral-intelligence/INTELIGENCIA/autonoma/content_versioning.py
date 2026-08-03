#!/usr/bin/env python3
"""Content Version Control — Git para videos: ramas, versiones, rollback."""
from __future__ import annotations
import argparse, json, hashlib, shutil
from pathlib import Path
from datetime import datetime

REPO = Path("results/version_history")
REPO.mkdir(parents=True, exist_ok=True)

def commit(video: str, mensaje: str = "", rama: str = "main"):
    src = Path(video)
    if not src.exists(): print("❌ No existe"); return
    h = hashlib.sha256(src.read_bytes()).hexdigest()[:12]
    ver_dir = REPO / rama / h
    ver_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, ver_dir / src.name)
    meta = {"archivo": src.name, "hash": h, "rama": rama, "mensaje": mensaje,
            "fecha": datetime.now().isoformat(), "tamano": src.stat().st_size}
    (ver_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"✅ Commit {h[:8]} en {rama}: {mensaje or src.name}")

def log(rama: str = "main", n: int = 10):
    rama_dir = REPO / rama
    if not rama_dir.exists(): print(f"❌ Rama '{rama}' no existe"); return
    commits = sorted(rama_dir.glob("*/meta.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:n]
    print(f"\n📜 Historial de '{rama}':\n")
    for c in commits:
        m = json.loads(c.read_text())
        print(f"  {m['hash'][:8]} | {m['fecha'][:19]} | {m['archivo']} | {m['mensaje'][:50]}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("accion", choices=["commit","log"])
    p.add_argument("--video","-v"); p.add_argument("--mensaje","-m",default="")
    p.add_argument("--rama","-b",default="main"); p.add_argument("--n",type=int,default=10)
    args = p.parse_args()
    if args.accion=="commit" and args.video: commit(args.video, args.mensaje, args.rama)
    else: log(args.rama, args.n)
