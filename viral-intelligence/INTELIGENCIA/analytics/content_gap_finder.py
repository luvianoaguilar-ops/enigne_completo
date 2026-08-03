#!/usr/bin/env python3
"""Content Gap Finder — detecta temas que nadie está cubriendo."""
from __future__ import annotations
import argparse, json
from pathlib import Path

TEMAS_POR_NICHO = {
    "finanzas": ["inversiones","crypto","ahorro","deudas","impuestos","freelance","jubilación","presupuesto","bolsa","bienes raíces"],
    "fitness": ["pesas","cardio","nutrición","flexibilidad","recuperación","suplementos","sueño","hidratación","postura","mentalidad"],
    "cocina": ["postres","meal prep","cocina rápida","vegetariano","air fryer","panadería","salsas","maridaje","conservas","batch cooking"],
    "tech": ["AI","programación","hardware","apps","ciberseguridad","cloud","blockchain","IoT","robótica","dev tools"],
    "productividad": ["GTD","hábitos","notion","minimalismo","time blocking","procrastinación","delegar","energía","focus","journaling"],
}

def encontrar_gaps(nicho: str, mis_temas: list):
    todos = TEMAS_POR_NICHO.get(nicho, TEMAS_POR_NICHO["productividad"])
    gaps = [t for t in todos if t not in [x.lower() for x in mis_temas]]
    
    print(f"\n🔍 CONTENT GAP FINDER — '{nicho}'\n")
    print(f"  📚 Temas totales del nicho: {len(todos)}")
    print(f"  ✅ Temás cubriendo:        {len(mis_temas)}")
    print(f"  🕳️ Gaps detectados:        {len(gaps)}\n")
    
    for i, g in enumerate(gaps, 1):
        dificultad = "🟢 Fácil" if len(g) < 8 else "🟡 Media" if len(g) < 12 else "🔴 Difícil"
        print(f"  {i:2d}. {g:20} {dificultad} | Primer video: 'Lo básico de {g} en 30s'")
    
    # Top 3 recomendados
    print(f"\n  🎯 TOP 3 GAPS PRIORITARIOS:")
    for g in gaps[:3]:
        print(f"     → {g} — Alta oportunidad, poca competencia percibida")
    return gaps

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("nicho"); p.add_argument("--temas", nargs="*", default=[])
    args = p.parse_args()
    encontrar_gaps(args.nicho, args.temas or ["general"])
