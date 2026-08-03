#!/usr/bin/env python3
"""Laboratorio A/B — genera variantes de hook, ritmo o color."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from datetime import datetime
from .utils import RESULTS_DIR, guardar_json

def variante(reporte, tipo, nombre):
    rec = reporte.get("receta",{})
    var = {"original":rec, "variante":{}, "tipo":tipo,
           "fecha":datetime.now().isoformat(), "notas":""}
    if tipo=="hook":
        sc = rec.get("hook",{}).get("score",0.5)
        var["variante"]["hook"] = {**rec.get("hook",{}),
            "score":min(1.0,sc+0.2),
            "nota":"Hook reforzado" if random.random()>0.5 else "Hook sutil"}
        var["notas"] = "Variar impacto visual primeros 1.5s"
    elif tipo=="ritmo":
        dm = rec.get("estructura",{}).get("duracion_media_toma",2.0)
        var["variante"]["duracion_media_toma"] = max(0.5, dm*0.8)
        var["notas"] = f"Reducir tomas de {dm:.1f}s a {var['variante']['duracion_media_toma']:.1f}s"
    elif tipo=="color":
        look = rec.get("look_visual", rec.get("look", {}))
        br = look.get("brillo_referencia", look.get("brillo", 50))
        var["variante"]["look_visual"] = {**look, "brillo_referencia":min(100,br+5)}
        var["notas"] = "Aumentar brillo para móviles"
    else:
        return {"error":"Tipo inválido"}
    salida = RESULTS_DIR/f"{nombre}_ab_{tipo}.json"
    guardar_json(str(salida), var)
    print(f"✅ Variante A/B: {salida}")
    return var

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("reporte")
    parser.add_argument("--tipo", choices=["hook","ritmo","color"], required=True)
    args = parser.parse_args()
    rep = json.load(open(args.reporte))
    nb = Path(args.reporte).stem.replace("_analisis","")
    variante(rep, args.tipo, nb)
