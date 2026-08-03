#!/usr/bin/env python3
"""Content Series Architect — diseña series de 10+ partes con cliffhangers."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from datetime import datetime

ESTRUCTURAS = {
    "tutorial": ["Introducción al concepto", "Materiales necesarios", "Paso 1: Fundamentos",
                  "Paso 2: Técnica principal", "Paso 3: Detalles avanzados", "Errores comunes",
                  "Trucos de experto", "Variaciones creativas", "Proyecto final parte 1",
                  "Proyecto final parte 2 + conclusión"],
    "historia": ["El inicio: personaje y contexto", "El problema aparece", "Primer intento fallido",
                  "Descubrimiento inesperado", "El punto más bajo", "Aliado inesperado",
                  "Segundo intento", "El clímax", "La revelación", "El desenlace + moraleja"],
    "lista": ["#1 El más obvio", "#2 El que todos ignoran", "#3 El controversial",
              "#4 El más caro", "#5 El más fácil", "#6 El más difícil",
              "#7 El secreto mejor guardado", "#8 El que cambiará todo",
              "#9 El más subestimado", "#10 El definitivo"],
    "viaje": ["Día 1: La decisión", "Día 2: Primer obstáculo", "Día 3-4: Adaptación",
              "Día 5: Crisis", "Día 7: Descubrimiento", "Día 10: La rutina",
              "Día 15: Resultados visibles", "Día 21: Nuevo hábito formado",
              "Día 28: Transformación", "Día 30: Reflexión final"],
}

def generar_serie(tema: str, tipo: str = "tutorial", episodios: int = 10):
    base = ESTRUCTURAS.get(tipo, ESTRUCTURAS["tutorial"])

    plan = {
        "serie": tema, "tipo": tipo, "total_episodios": episodios,
        "generado": datetime.now().isoformat(), "episodios": []
    }

    for i, titulo in enumerate(base[:episodios], 1):
        cliffhanger = ""
        if i < episodios:
            cliffhanger = f"En el próximo episodio: {base[i][:60]}... No te lo pierdas."
        plan["episodios"].append({
            "numero": i, "titulo": f"{titulo} — {tema}",
            "formato": "TikTok/Reels/Shorts", "duracion_estimada": "30-60s",
            "cta": "Seguime para la parte "+str(i+1) if i<episodios else "Comentá tu experiencia",
            "cliffhanger": cliffhanger,
        })

    out = f"results/serie_{tema.replace(' ','_')[:30]}.json"
    Path(out).write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"✅ Serie creada: {out}\n")
    for ep in plan["episodios"]:
        print(f"  Ep {ep['numero']:2d}: {ep['titulo']}")
        if ep['cliffhanger']: print(f"         🔗 {ep['cliffhanger'][:80]}")
    return plan

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("tema"); p.add_argument("--tipo",default="tutorial",
        choices=["tutorial","historia","lista","viaje"]); p.add_argument("--episodios",type=int,default=10)
    args = p.parse_args()
    generar_serie(args.tema, args.tipo, args.episodios)
