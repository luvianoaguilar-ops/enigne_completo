#!/usr/bin/env python3
"""AI Script Doctor — analiza guiones y sugiere mejoras de ritmo, gancho y emoción."""
from __future__ import annotations
import argparse, re, json
from pathlib import Path

def analizar_guion(texto: str) -> dict:
    palabras = len(re.findall(r'\b\w+\b', texto))
    oraciones = len(re.findall(r'[.!?]+', texto))
    hooks = re.findall(r'(?:sabias que|imaginate|esto es|nadie te dice|el secreto|mirá|atencion|error|para|dejá de)', texto.lower())
    preguntas = len(re.findall(r'\?', texto))
    exclamaciones = len(re.findall(r'!', texto))
    cta = bool(re.search(r'(?:seguime|comentá|like|guardá|compartí|link en bio)', texto.lower()))
    
    score = 0
    recs = []
    if len(hooks) > 0: score += 25; recs.append("✅ Tiene gancho identificable")
    else: recs.append("⚠️ Agregá un gancho fuerte al inicio")
    if 5 <= oraciones <= 15: score += 15; recs.append("✅ Buena cantidad de oraciones")
    elif oraciones < 3: recs.append("⚠️ Muy pocas oraciones, desarrollá más")
    else: recs.append("⚠️ Demasiadas oraciones, simplificá")
    if preguntas >= 1: score += 10; recs.append("✅ Usa preguntas para engagement")
    if exclamaciones >= 2: score += 10; recs.append("✅ Energía con exclamaciones")
    if cta: score += 15; recs.append("✅ Tiene call-to-action")
    else: recs.append("⚠️ Falta CTA al final")
    if 15 <= palabras <= 80: score += 15; recs.append("✅ Longitud de guion óptima")
    else: recs.append("⚠️ Ajustá longitud (ideal: 15-80 palabras)")
    
    nivel = "🔥 Listo para grabar" if score>=70 else "📝 Necesita ajustes" if score>=45 else "🔴 Requiere reescritura"
    return {"score": min(100, score+10), "nivel": nivel, "metricas": {
        "palabras": palabras, "oraciones": oraciones, "preguntas": preguntas,
        "exclamaciones": exclamaciones, "tiene_hook": len(hooks)>0, "tiene_cta": cta},
        "recomendaciones": recs, "hooks_detectados": hooks}

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("guion"); args = p.parse_args()
    texto = Path(args.guion).read_text(encoding="utf-8")
    r = analizar_guion(texto)
    print(json.dumps(r, indent=2, ensure_ascii=False))
