#!/usr/bin/env python3
"""Voice Energy Calibrator — analiza y recomienda ajustes de energía vocal."""
from __future__ import annotations
import argparse, json
from pathlib import Path

NIVELES = {
    "muy_baja": {"score": (0,20), "recomendacion": "⚠️ Urgente: subí la energía. Imaginate contándoselo a un amigo."},
    "baja": {"score": (21,40), "recomendacion": "📝 Aumentá variación de tono. Usá más preguntas y exclamaciones."},
    "media": {"score": (41,65), "recomendacion": "✅ Buena base. Agregá picos de energía cada 5-7 segundos."},
    "alta": {"score": (66,85), "recomendacion": "🔥 Excelente energía. Cuidado con saturar."},
    "muy_alta": {"score": (86,100), "recomendacion": "⚡ Energía máxima. Ideal para hooks y CTAs."},
}

def calibrar(texto_guion: str, bpm_objetivo: int = 120):
    palabras = len(texto_guion.split())
    frases = texto_guion.count(".") + texto_guion.count("!") + texto_guion.count("?")
    exclamaciones = texto_guion.count("!")
    preguntas = texto_guion.count("?")
    
    score = min(100, 30 + exclamaciones*10 + preguntas*8 + min(30, frases*4))
    if bpm_objetivo >= 130: score += 10
    elif bpm_objetivo < 100: score = max(0, score - 10)
    
    nivel = next(k for k, v in NIVELES.items() if v["score"][0] <= score <= v["score"][1])
    info = NIVELES[nivel]
    
    r = {"score_energia": score, "nivel": nivel, "recomendacion": info["recomendacion"],
         "metricas": {"palabras": palabras, "frases": frases, "exclamaciones": exclamaciones,
                      "preguntas": preguntas, "bpm_objetivo": bpm_objetivo},
         "sugerencias": [
             "Grabá 3 versiones con distinta energía y compará",
             "Marcá en el guion dónde SUBIR y dónde BAJAR la energía",
             "Usá las manos al hablar (se nota en la voz)",
         ]}
    print(f"\n🎤 VOICE ENERGY CALIBRATOR\n")
    print(f"  Score: {score}/100 — {nivel.upper().replace('_',' ')}")
    print(f"  {info['recomendacion']}")
    print(f"\n  💡 Sugerencias:")
    for s in r["sugerencias"]: print(f"     • {s}")
    return r

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("guion"); p.add_argument("--bpm",type=int,default=120)
    args = p.parse_args()
    texto = Path(args.guion).read_text() if Path(args.guion).exists() else args.guion
    calibrar(texto, args.bpm)
