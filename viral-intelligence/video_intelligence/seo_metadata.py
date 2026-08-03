#!/usr/bin/env python3
"""Generador de metadatos SEO — títulos, descripción, tags."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def generar_seo(reporte, concepto):
    dur = reporte.get("metadatos",{}).get("duracion_segundos",0)
    ritmo = reporte.get("visual",{}).get("edicion",{}).get("estadisticas_tomas",{}).get("ritmo","dinámico")
    titulos = [
        f"El secreto de {concepto} que nadie te cuenta 🤯",
        f"Cómo dominar {concepto} en {int(dur)}s 🚀",
        f"Lo que pasa cuando intentas {concepto} 🔥",
        f"La verdad sobre {concepto} (Paso a paso) ✨"
    ]
    desc = (f"¿Te interesa {concepto}? En este video exploramos los puntos clave con ritmo {ritmo}.\n"
            f"📌 Lo que verás:\n- Análisis detallado\n- Tips prácticos\n"
            f"- Cierre con conclusión\n#shorts #viral #{concepto.replace(' ','')}")
    tags = [concepto, f"como hacer {concepto}", "tutorial rapido", "shorts", "viral", "tips", ritmo]
    res = {"concepto":concepto, "titulos":titulos, "descripcion":desc, "tags":tags}
    salida = RESULTS_DIR / f"{Path(reporte).stem}_seo.json" if isinstance(reporte,str) else RESULTS_DIR/"seo_output.json"
    guardar_json(str(salida), res)
    print(f"✅ SEO: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reporte")
    parser.add_argument("--concepto", required=True)
    args = parser.parse_args()
    rep = json.load(open(args.reporte))
    generar_seo(rep, args.concepto)
