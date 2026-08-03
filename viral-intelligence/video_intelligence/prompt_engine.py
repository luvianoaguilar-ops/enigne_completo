#!/usr/bin/env python3
"""Factory de prompts — genera 5 tipos de prompts desde la receta técnica."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def crear_prompts(reporte, concepto):
    receta = reporte.get("receta", {})
    look = receta.get("look", {})
    dur = receta.get("duracion_media_toma", 2.0) * 10
    ritmo = receta.get("ritmo_edicion", "medio")
    bpm = receta.get("bpm_referencia", 0)
    cam = receta.get("movimiento_camara", "suave")
    fmt = receta.get("formato", "vertical")
    base = (f"Crear pieza audiovisual original sobre: {concepto}. "
            f"Formato {fmt}, ~{dur}s. Ritmo {ritmo}. "
            f"Cámara: {cam}. BPM ref: {bpm}. "
            f"Brillo {look.get('brillo','N/A')}, contraste {look.get('contraste','N/A')}. "
            f"Mantener coherencia, anatomía correcta, texto legible, composición segura móvil. "
            f"No copiar personajes/marcas/voces.")
    return {
        "director": f"{base}\nDiseñar: 1.Hook 0-1.5s, 2.Presentación, 3.Desarrollo, 4.Clímax, 5.Cierre.",
        "video_ia": f"{base}\nGenerar video original con continuidad, iluminación consistente, sin flicker.",
        "imagen_ia": f"Crear imagen original para: {concepto}. Composición {fmt}, espacio negativo para titular.",
        "editor": f"Actúa como editor: {concepto}, {dur}s, ritmo {ritmo}, música ~{bpm}BPM. Timecodes + cortes + beats.",
        "critico": f"Evalúa pieza sobre {concepto}. Puntúa 0-100: hook, claridad, composición, continuidad, ritmo, sincronía, legibilidad, audio, originalidad, cierre."
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reporte")
    parser.add_argument("--concepto", required=True)
    args = parser.parse_args()
    rep = json.load(open(args.reporte))
    prompts = crear_prompts(rep, args.concepto)
    salida = RESULTS_DIR / f"{Path(args.reporte).stem}_prompts.json"
    guardar_json(str(salida), prompts)
    print(f"✅ Prompts: {salida}")
