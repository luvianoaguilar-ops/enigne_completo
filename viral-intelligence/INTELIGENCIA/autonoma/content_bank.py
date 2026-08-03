#!/usr/bin/env python3
"""Content Bank Autopilot — genera 90 días de contenido automáticamente."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from datetime import datetime, timedelta

TIPOS = ["Tutorial", "Storytime", "Top 5", "Mito vs Realidad", "Día en mi vida",
         "Review", "Comparativa", "Antes/Después", "Detrás de escena", "Q&A"]

EMOCIONES = ["curiosidad", "urgencia", "empatía", "humor", "inspiración", "sorpresa"]

def generar_banco(tema: str, dias: int = 90):
    plan = {"tema": tema, "generado": datetime.now().isoformat(),
            "total_dias": dias, "calendario": []}
    fecha = datetime.now()
    for d in range(dias):
        tipo = TIPOS[d % len(TIPOS)]
        emocion = EMOCIONES[d % len(EMOCIONES)]
        variante = f"Parte {(d//7)+1}" if d % 7 == 0 else f"Variante {random.randint(1,5)}"
        plan["calendario"].append({
            "dia": d+1, "fecha": (fecha + timedelta(days=d)).strftime("%Y-%m-%d"),
            "tipo": tipo, "emocion": emocion, "variante": variante,
            "gancho_sugerido": f"Lo que aprendí sobre {tema} — {variante}",
            "formato": "TikTok/Reels/Shorts", "duracion": "30-60s",
        })
    out = f"results/content_bank_{tema.replace(' ','_')[:30]}_{dias}dias.json"
    Path(out).write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    
    # Print summary
    tipos_count = {}
    for e in plan["calendario"]: tipos_count[e["tipo"]] = tipos_count.get(e["tipo"], 0) + 1
    print(f"✅ Banco de {dias} días para '{tema}'\n")
    print("📊 DISTRIBUCIÓN:")
    for t, c in sorted(tipos_count.items(), key=lambda x: -x[1]):
        bar = "█"*(c//5)+"░"*(18-c//5)
        print(f"  {t:20} |{bar}| {c:3d} videos")
    print(f"\n📁 Guardado: {out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("tema"); p.add_argument("--dias",type=int,default=90)
    args = p.parse_args()
    generar_banco(args.tema, args.dias)
