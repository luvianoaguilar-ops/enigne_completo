#!/usr/bin/env python3
"""Emotion Arc Designer — diseña la curva emocional segundo a segundo."""
from __future__ import annotations
import argparse, json, math
from pathlib import Path

EMOCIONES = ["curiosidad", "sorpresa", "tensión", "alivio", "urgencia", "empatía", "humor", "inspiración"]

def disenar_arco(duracion: int = 30, intensidad: str = "alta"):
    arco = []
    for s in range(duracion+1):
        pct = s / duracion
        if s <= 2:
            valor = 8.5 if intensidad == "alta" else 6.5
            emocion = "sorpresa"
        elif s <= 5:
            valor = 7.0 - (s-2)*0.5
            emocion = "curiosidad"
        elif s <= duracion*0.6:
            valor = 5.5 + 1.5*math.sin((s-5)*0.4)
            emocion = "tensión" if valor>6 else "empatía"
        elif s <= duracion-3:
            valor = 8.0 + 1.0*math.cos((s-duracion*0.6)*0.8)
            emocion = "urgencia" if s<duracion-6 else "inspiración"
        else:
            valor = 7.5 - (duracion-s)*1.5
            emocion = "inspiración"
        valor = max(1, min(10, round(valor, 1)))
        arco.append({"segundo": s, "intensidad": valor, "emocion": emocion,
                     "accion": "Mantener" if valor>6 else "Acelerar ritmo" if valor<4 else "Desarrollar",
                     "texto_sugerido": "Gancho potente" if s<=2 else "CTA final" if s>=duracion-2 else ""})
    return arco

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--duracion",type=int,default=30)
    p.add_argument("--intensidad",default="alta",choices=["baja","media","alta"])
    args = p.parse_args()
    arco = disenar_arco(args.duracion, args.intensidad)
    out = f"results/emotion_arc_{args.duracion}s.json"
    Path(out).write_text(json.dumps({"duracion": args.duracion, "intensidad": args.intensidad, "arco": arco}, indent=2))
    print(f"✅ Arco emocional guardado: {out}")
    print(f"\n📈 Curva para {args.duracion}s ({args.intensidad} intensidad):")
    for p in arco[::max(1, args.duracion//10)]:
        bar = "█"*int(p["intensidad"])+"░"*(10-int(p["intensidad"]))
        print(f"  {p['segundo']:3d}s |{bar}| {p['intensidad']:.1f} — {p['emocion']}")
