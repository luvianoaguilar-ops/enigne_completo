#!/usr/bin/env python3
"""Community Co-Creator — la comunidad vota qué contenido crear."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path

def generar_encuesta(tema: str, opciones: int = 4):
    formatos = ["Tutorial paso a paso", "Top 5 errores", "Storytime personal", 
                "Comparativa", "Mitos vs Realidad", "Día en mi vida", "Review honesto"]
    angulos = [f"Cómo empecé en {tema}", f"Lo más difícil de {tema}", f"Mi rutina de {tema}",
               f"Inversión necesaria para {tema}", f"Errores que cometí en {tema}",
               f"Resultados después de 30 días de {tema}"]
    opciones_gen = []
    for i in range(opciones):
        fmt = random.choice(formatos)
        ang = random.choice(angulos)
        opciones_gen.append({"id": i+1, "formato": fmt, "angulo": ang,
                             "titulo_votacion": f"{fmt}: {ang}"})
    encuesta = {"tema": tema, "opciones": opciones_gen,
                "instruccion": "Votá en comentarios: A, B, C o D",
                "hashtags": ["#comunidad","#votacion",f"#{tema.replace(' ','')}"]}
    out = f"results/encuesta_{tema.replace(' ','_')[:30]}.json"
    Path(out).write_text(json.dumps(encuesta, indent=2, ensure_ascii=False))
    print("🗳️ ENCUESTA PARA LA COMUNIDAD:\n")
    for o in opciones_gen:
        letra = chr(64+o["id"])
        print(f"  {letra}) {o['titulo_votacion']}")
    print(f"\n✅ Guardada: {out}")
    return encuesta

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("tema"); p.add_argument("--opciones",type=int,default=4)
    args = p.parse_args()
    generar_encuesta(args.tema, args.opciones)
