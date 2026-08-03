#!/usr/bin/env python3
"""Smart Content Recycler — re-empaqueta contenido viejo con nuevos ganchos."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from datetime import datetime

NUEVOS_GANCHOS = [
    "¿Viste esto hace 3 meses? Mirá lo que pasó después...",
    "Actualización: lo que aprendí sobre {tema}",
    "Volví a intentar {tema} y esto cambió TODO",
    "3 cosas que hago diferente con {tema} ahora",
    "Lo que NADIE te dijo sobre {tema} (parte 2)",
    "Un año después: ¿valió la pena {tema}?",
    "El antes y después de {tema} es increíble",
]

NUEVOS_FORMATOS = ["Antes vs Después", "Reaction a mi yo del pasado", "Actualización rápida",
                   "Lo que haría diferente", "Top 3 aprendizajes", "Respondiendo preguntas"]

def reciclar(adn_json: str, tema: str, cantidad: int = 5):
    adn = json.loads(Path(adn_json).read_text()) if Path(adn_json).exists() else {}
    ideas = []
    for i in range(cantidad):
        gancho = random.choice(NUEVOS_GANCHOS).replace("{tema}", tema)
        formato = random.choice(NUEVOS_FORMATOS)
        ideas.append({"id": i+1, "gancho": gancho, "formato": formato,
                      "fuente": Path(adn_json).stem, "tema": tema,
                      "accion": f"Regrabar manteniendo estructura pero con {formato.lower()}"})
    
    out = f"results/recycled_{tema.replace(' ','_')[:30]}.json"
    Path(out).write_text(json.dumps({"tema_original": tema, "fecha": datetime.now().isoformat(),
                                      "ideas_recicladas": ideas}, indent=2, ensure_ascii=False))
    print(f"✅ {cantidad} ideas recicladas: {out}\n")
    for idea in ideas: print(f"  {idea['id']}. [{idea['formato']}] {idea['gancho']}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--adn",default=""); p.add_argument("--tema",required=True)
    p.add_argument("--cantidad",type=int,default=5); args = p.parse_args()
    reciclar(args.adn, args.tema, args.cantidad)
