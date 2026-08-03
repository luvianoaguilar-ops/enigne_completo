#!/usr/bin/env python3
"""Content Health Dashboard — salud de todo tu catálogo de contenido."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime, timedelta

def evaluar_salud(dataset_dir: str):
    d = Path(dataset_dir)
    if not d.exists(): return {"error": "Directorio no encontrado"}
    adns = list(d.glob("*/adn_video.json"))
    if not adns: return {"error": "Sin ADNs", "videos": 0}

    scores = []
    for adn_file in adns:
        data = json.loads(adn_file.read_text())
        cpm = data.get("estadisticas", {}).get("cortes_por_minuto", 0)
        bpm = data.get("audio", {}).get("bpm", 0)
        dur = data.get("metadata", {}).get("duracion_segundos", 60)
        esc = len(data.get("escenas", []))
        s = min(100, cpm*3 + (20 if 110<=bpm<=145 else 10) + (20 if 7<=dur<=34 else 10) + esc*2)
        scores.append(s)

    avg = sum(scores)/len(scores) if scores else 0
    above = sum(1 for s in scores if s > 70)
    stale = sum(1 for s in scores[-10:] if s < 40) if len(scores)>10 else 0

    salud = {
        "total_videos": len(adns), "score_promedio": round(avg, 1),
        "videos_saludables": above, "videos_en_riesgo": stale,
        "salud_general": "🟢 EXCELENTE" if avg>=70 else "🟡 ESTABLE" if avg>=50 else "🔴 NECESITA ATENCIÓN",
        "recomendacion": "Seguí así, tu contenido es sólido" if avg>=70 else
                         "Revisá ganchos y CPM de los últimos videos" if avg>=50 else
                         "URGENTE: replanteá tu estrategia de contenido",
        "tendencia": "📈 Mejorando" if scores and scores[-1]>scores[0] else "📉 Cuidado" if scores and scores[-1]<scores[0]*0.7 else "➡️ Estable"
    }
    out = Path("results/content_health.json")
    out.write_text(json.dumps(salud, indent=2, ensure_ascii=False))
    print(f"\n🏥 CONTENT HEALTH: {salud['salud_general']}")
    print(f"   📹 {salud['total_videos']} videos | ⭐ {salud['score_promedio']}/100")
    print(f"   ✅ {salud['videos_saludables']} saludables | ⚠️ {salud['videos_en_riesgo']} en riesgo")
    print(f"   📊 {salud['tendencia']} | 💡 {salud['recomendacion']}")
    return salud

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("dataset", nargs="?", default="data/dataset")
    args = p.parse_args()
    evaluar_salud(args.dataset)
