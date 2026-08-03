#!/usr/bin/env python3
"""Collaboration Opportunity Radar — detecta creators ideales para collab."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def evaluar_compatibilidad(mi_nicho: str, mi_estilo: str, candidates: list) -> list:
    nichos_comp = {"finanzas": ["emprendimiento","inversiones","tech","educación"],
                   "fitness": ["nutrición","salud","deportes","bienestar"],
                   "cocina": ["lifestyle","familia","salud","viajes"],
                   "tech": ["AI","programación","gadgets","finanzas"],
                   "productividad": ["hábitos","negocios","educación","lifestyle"]}
    compatibles = nichos_comp.get(mi_nicho, [mi_nicho])
    results = []
    for c in candidates:
        score = 0
        if c.get("nicho") in compatibles: score += 40
        if c.get("estilo") == mi_estilo: score += 20
        overlap = len(set(c.get("temas",[])) & set(compatibles))
        score += overlap * 10
        if score >= 30:
            results.append({**c, "compatibilidad": min(100, score+20),
                           "idea_collab": f"Hacer un {c.get('formato_fuerte','duo')} sobre {mi_nicho} y {c.get('nicho')}"})
    return sorted(results, key=lambda x: x["compatibilidad"], reverse=True)

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--nicho",required=True)
    p.add_argument("--estilo",default="educativo"); p.add_argument("--candidates",default="[]")
    args = p.parse_args()
    # Demo candidates
    demo = [
        {"nombre":"CreadorA","nicho":"emprendimiento","estilo":"educativo","formato_fuerte":"duo","temas":["negocios","inversiones"]},
        {"nombre":"CreadorB","nicho":"bienestar","estilo":"storytime","formato_fuerte":"stitch","temas":["salud","hábitos"]},
        {"nombre":"CreadorC","nicho":"tech","estilo":"educativo","formato_fuerte":"duo","temas":["AI","gadgets","inversiones"]},
        {"nombre":"CreadorD","nicho":"comedia","estilo":"entretenimiento","formato_fuerte":"challenge","temas":["humor"]},
    ]
    results = evaluar_compatibilidad(args.nicho, args.estilo, demo)
    print(f"\n📡 COLLAB RADAR para '{args.nicho}' ({args.estilo}):\n")
    for r in results:
        bar = "█"*min(10, r["compatibilidad"]//10)+"░"*(10-min(10, r["compatibilidad"]//10))
        print(f"  {r['nombre']:15} |{bar}| {r['compatibilidad']}% | {r['idea_collab']}")
