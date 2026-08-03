#!/usr/bin/env python3
"""Audience Persona Generator — genera personas de audiencia desde datos."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path

INTERESES = {"finanzas": ["inversión","ahorro","crypto","trading","educación financiera"],
    "fitness": ["gym","nutrición","running","yoga","pesas"],
    "tech": ["AI","programación","gadgets","startups","ciberseguridad"],
    "cocina": ["recetas","meal prep","pastelería","cocina saludable","air fryer"],
    "productividad": ["hábitos","notion","GTD","minimalismo","time blocking"]}

PLATAFORMAS = ["TikTok 2h/día","Instagram 1.5h/día","YouTube 1h/día","Twitter 45min/día"]
DOLORES = ["No tengo tiempo","Es muy caro","No sé por dónde empezar","Ya intenté y fallé","Es demasiado técnico"]

def generar(nicho: str, cantidad: int = 3):
    intereses = INTERESES.get(nicho, ["aprender","mejorar","crecer"])
    personas = []
    nombres = ["María", "Carlos", "Lucía", "Javier", "Ana", "Diego", "Sofía", "Pablo"]
    for i in range(min(cantidad, len(nombres))):
        p = {"nombre": nombres[i], "edad": random.randint(18, 45),
             "nicho": nicho, "nivel": random.choice(["principiante","intermedio","avanzado"]),
             "intereses": random.sample(intereses, min(3, len(intereses))),
             "plataformas": random.sample(PLATAFORMAS, 2),
             "dolor_principal": random.choice(DOLORES),
             "objetivo": f"Quiere dominar {random.choice(intereses)} en menos de 30 días",
             "tipo_contenido_favorito": random.choice(["tutorial rápido","storytime","lista top","detrás de escena"]),
             "mejor_horario": f"{random.randint(18,22)}hs (después del trabajo)"}
        personas.append(p)
    out = f"results/personas_{nicho}.json"
    Path(out).write_text(json.dumps({"nicho": nicho, "personas": personas}, indent=2, ensure_ascii=False))
    print(f"✅ {len(personas)} personas generadas: {out}\n")
    for p in personas:
        print(f"  👤 {p['nombre']} ({p['edad']}) — {p['nivel']} | Duele: {p['dolor_principal']} | Hora: {p['mejor_horario']}")
    return personas

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("nicho"); p.add_argument("--cantidad",type=int,default=3)
    args = p.parse_args()
    generar(args.nicho, args.cantidad)
