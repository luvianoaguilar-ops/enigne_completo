#!/usr/bin/env python3
"""Content Repurposing Chain — 1 long-form → 5 shorts → 10 tweets → 1 blog → 20 clips."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime

def generar_cadena(tema: str, puntos_clave: list = None):
    if puntos_clave is None: puntos_clave = ["Introducción","Problema principal","Solución","Resultado","Conclusión"]
    cadena = {
        "fuente": tema, "generado": datetime.now().isoformat(),
        "long_form": {"formato": "YouTube 5-10min", "estructura": [f"{i+1}. {p}" for i,p in enumerate(puntos_clave)]},
        "shorts": [],
        "tweets": [],
        "clips": [],
    }
    for i, punto in enumerate(puntos_clave):
        cadena["shorts"].append({"plataforma": ["TikTok","Reels","Shorts"][i%3],
            "gancho": f"El secreto de {punto.lower()} que nadie te cuenta",
            "duracion": "15-30s", "contenido": f"Clip sobre: {punto}"})
        cadena["tweets"].append(f"{i+1}/ {punto} — Hilo sobre {tema} 🧵")
        cadena["clips"].append({"segundo_inicio": i*90, "segundo_fin": (i+1)*90,
            "descripcion": f"Clip {i+1}: {punto}"})

    out = f"results/repurpose_{tema.replace(' ','_')[:30]}.json"
    Path(out).write_text(json.dumps(cadena, indent=2, ensure_ascii=False))
    print(f"✅ Cadena de repurposing generada:\n")
    print(f"  🎬 1 Long-form → {len(cadena['shorts'])} Shorts")
    print(f"  🐦 {len(cadena['tweets'])} Tweets")
    print(f"  ✂️ {len(cadena['clips'])} Clips\n📁 {out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("tema"); p.add_argument("--puntos",nargs="*")
    args = p.parse_args()
    generar_cadena(args.tema, args.puntos)
