#!/usr/bin/env python3
"""Viral Trajectory Simulator — simula trayectorias de engagement."""
from __future__ import annotations
import argparse, json, math, random
from pathlib import Path

def simular(score_base: int, dias: int = 7, simulaciones: int = 10):
    resultados = []
    for sim in range(simulaciones):
        ruido = random.gauss(0, 8)
        trayectoria = []
        vistas = 100
        pico = random.randint(2, 5)
        for d in range(1, dias+1):
            factor = 1.0
            if d <= 2: factor = 1.3 + score_base/200  # Crecimiento inicial
            elif d == pico: factor = 2.0 + score_base/150  # Pico viral
            elif d > pico: factor = 0.7 - d*0.03  # Decay
            factor += random.gauss(0, 0.15)
            vistas = max(0, int(vistas * max(0.3, factor)))
            trayectoria.append({"dia": d, "vistas_estimadas": vistas})
        resultados.append({"simulacion": sim+1, "pico_dia": pico, "trayectoria": trayectoria})
    
    # Promedio de vistas totales
    totales = [sum(t["vistas_estimadas"] for t in r["trayectoria"]) for r in resultados]
    avg = sum(totales)/len(totales)
    
    reporte = {"score_base": score_base, "dias": dias, "simulaciones": simulaciones,
               "promedio_vistas_totales": int(avg),
               "rango": [int(min(totales)), int(max(totales))],
               "nivel": "🚀 POTENCIAL VIRAL" if avg>50000 else "🔥 ALTO" if avg>10000 else "📊 PROMEDIO",
               "trayectorias": resultados}
    
    out = f"results/viral_sim_{score_base}.json"
    Path(out).write_text(json.dumps(reporte, indent=2))
    print(f"\n🔮 VIRAL TRAJECTORY SIMULATOR\n")
    print(f"  Score base: {score_base}/100 | {simulaciones} simulaciones × {dias} días")
    print(f"  📈 Vistas promedio totales: {int(avg):,}")
    print(f"  📊 Rango: {int(min(totales)):,} — {int(max(totales)):,}")
    print(f"  {reporte['nivel']}")
    return reporte

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("score", type=int); p.add_argument("--dias", type=int, default=7)
    p.add_argument("--sims", type=int, default=10)
    args = p.parse_args()
    simular(args.score, args.dias, args.sims)
