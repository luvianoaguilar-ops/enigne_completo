#!/usr/bin/env python3
"""Best Time to Post Calculator — calcula horario óptimo para publicar."""
from __future__ import annotations
import argparse, json
from pathlib import Path

HORARIOS_POR_NICHO = {
    "finanzas": [(7,9),(12,14),(19,21)], "fitness": [(6,8),(12,13),(18,20)],
    "cocina": [(10,12),(15,17),(19,21)], "tech": [(8,10),(13,15),(20,22)],
    "productividad": [(6,8),(12,14),(20,22)], "entretenimiento": [(12,14),(18,21),(21,23)],
    "educacion": [(7,9),(15,17),(20,22)], "general": [(7,9),(12,14),(19,21)]
}

DIAS = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
PESOS = [0.9, 1.0, 1.1, 1.05, 0.8, 0.6, 1.15]  # Domingo y Miércoles rinden más

def calcular(nicho: str = "general"):
    rangos = HORARIOS_POR_NICHO.get(nicho, HORARIOS_POR_NICHO["general"])
    plan = []
    for i, (dia, peso) in enumerate(zip(DIAS, PESOS)):
        slots = []
        for ini, fin in rangos:
            score = round(min(100, 55 + peso*25 + (5 if 18<=ini<=21 else 0) + (3 if i in [5,6] else 0)))
            slots.append({"hora": f"{ini}:00-{fin}:00", "score": score,
                          "nivel": "🌟 ÓPTIMO" if score>=80 else "✅ Bueno" if score>=65 else "📊 Regular"})
        plan.append({"dia": dia, "slots": slots})
    
    print(f"\n⏰ MEJORES HORARIOS PARA '{nicho}':\n")
    for p in plan:
        best = max(p["slots"], key=lambda s: s["score"])
        print(f"  {p['dia']:10} → {best['hora']:12} ⭐{best['score']} {best['nivel']}")
    
    recomendacion = max(((p["dia"], s) for p in plan for s in p["slots"]), key=lambda x: x[1]["score"])
    print(f"\n  🎯 MEJOR MOMENTO: {recomendacion[0]} {recomendacion[1]['hora']} (score: {recomendacion[1]['score']})")
    return plan

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("nicho", nargs="?", default="general")
    args = p.parse_args()
    calcular(args.nicho)
