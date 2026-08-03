#!/usr/bin/env python3
"""Hashtag Optimizer — estrategia de hashtag ladder por nicho."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path

HASHTAGS_POOL = {
    "finanzas": {"masivo": ["#fyp","#viral","#dinero"], "medio": ["#finanzas","#inversiones","#educacionfinanciera"], "bajo": ["#libertadfinanciera","#ahorrointeligente","#tradingparaprincipiantes"]},
    "fitness": {"masivo": ["#fyp","#viral","#gym"], "medio": ["#fitness","#workout","#motivation"], "bajo": ["#fitnesstips","#gymrat","#homeworkout"]},
    "cocina": {"masivo": ["#fyp","#viral","#food"], "medio": ["#cocina","#recetas","#foodie"], "bajo": ["#recetasfaciles","#mealprep","#cocinasaludable"]},
    "tech": {"masivo": ["#fyp","#viral","#tech"], "medio": ["#tecnologia","#programacion","#ia"], "bajo": ["#devlife","#startups","#ciberseguridad"]},
    "productividad": {"masivo": ["#fyp","#viral","#motivation"], "medio": ["#productividad","#habitos","#disciplina"], "bajo": ["#productivitytips","#notion","#timemanagement"]},
}

def optimizar(nicho: str, contenido: str = ""):
    pool = HASHTAGS_POOL.get(nicho, HASHTAGS_POOL["productividad"])
    seleccion = {
        "masivos": random.sample(pool["masivo"], min(2, len(pool["masivo"]))),
        "medios": random.sample(pool["medio"], min(3, len(pool["medio"]))),
        "bajos": random.sample(pool["bajo"], min(3, len(pool["bajo"]))),
    }
    todos = seleccion["masivos"] + seleccion["medios"] + seleccion["bajos"]
    print(f"\n#️⃣ HASHTAGS PARA '{nicho}':\n")
    print("  🔴 Masivos (competitivos): " + " ".join(seleccion["masivos"]))
    print("  🟡 Nicho (targeted):       " + " ".join(seleccion["medios"]))
    print("  🟢 Únicos (tu marca):      " + " ".join(seleccion["bajos"]))
    copiar = " ".join(todos)
    print(f"\n  📋 Copiar: {copiar}")
    return todos

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("nicho"); p.add_argument("--contenido",default="")
    args = p.parse_args()
    optimizar(args.nicho, args.contenido)
