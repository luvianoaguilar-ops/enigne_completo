#!/usr/bin/env python3
"""AB Testing Lab — genera y compara variantes de hooks, ritmo y color."""
from __future__ import annotations
import argparse, json, random
from pathlib import Path
from datetime import datetime

def generar_variantes(adn_json: str, n: int = 5):
    """Genera N variantes A/B para testing."""
    try:
        adn = json.loads(Path(adn_json).read_text())
    except: adn = {}
    
    variantes = {
        "hook": [],
        "ritmo": [],
        "audio": [],
        "texto": [],
        "color": [],
    }
    
    for i in range(n):
        variantes["hook"].append({
            "id": f"H{i+1}", "tipo": random.choice(["pregunta","shock","promesa","negacion","contraste"]),
            "texto": f"Variante hook {i+1}: {random.choice(['Sabías que','El secreto','Nadie te dice','Probé','Esto cambió'])}...",
        })
        variantes["ritmo"].append({
            "id": f"R{i+1}", "cpm": random.randint(10, 35),
            "estilo": "ultra-rápido" if random.random()>0.5 else "pausado-estratégico",
        })
        variantes["audio"].append({
            "id": f"A{i+1}", "bpm": random.randint(90, 160),
            "genero": random.choice(["lo-fi","energético","cinematic","ambiente","pop"]),
        })
        variantes["texto"].append({
            "id": f"T{i+1}", "estilo": random.choice(["bold grande","minimalista","karaoke","sin texto"]),
            "posicion": random.choice(["centro","inferior","superior","dinámico"]),
        })
        variantes["color"].append({
            "id": f"C{i+1}", "paleta": random.choice(["cálida","fría","alto contraste","pastel","oscura"]),
            "filtro": random.choice(["ninguno","vintage","clean","dramatic","natural"]),
        })

    reporte = {"fuente": Path(adn_json).stem, "fecha": datetime.now().isoformat(),
               "total_combinaciones": n**5, "variantes": variantes,
               "recomendacion_testing": "Testeá 3 combinaciones: mejor hook + mejor ritmo + mejor audio"}
    
    out = f"results/ab_lab_{Path(adn_json).stem}.json"
    Path(out).write_text(json.dumps(reporte, indent=2, ensure_ascii=False))
    print(f"🧪 AB TESTING LAB: {n} variantes × 5 dimensiones = {n**5} combinaciones posibles\n")
    for dim, vars_list in variantes.items():
        print(f"  📐 {dim.upper()}: {len(vars_list)} variantes → {vars_list[0]['id']}...{vars_list[-1]['id']}")
    print(f"\n📁 {out}")
    return reporte

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("adn", nargs="?", default="data/dataset")
    p.add_argument("--n", type=int, default=5)
    args = p.parse_args()
    generar_variantes(args.adn, args.n)
