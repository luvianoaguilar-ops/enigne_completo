#!/usr/bin/env python3
"""Drop-off Forensics — análisis forense de por qué la gente hace scroll."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def analizar(adn_json: str):
    d = json.loads(Path(adn_json).read_text())
    escenas = d.get("escenas", [])
    energia = d.get("audio", {})
    forense = []
    for i, esc in enumerate(escenas):
        riesgo = 0
        causas = []
        dur = esc.get("duracion_seg", 0)
        if dur > 3.5: riesgo += 30; causas.append(f"Escena larga ({dur:.1f}s)")
        if dur > 5: riesgo += 20; causas.append("ALERTA: escena >5s = scroll asegurado")
        if i == 0 and dur > 2: riesgo += 15; causas.append("Gancho lento")
        textos = esc.get("textos_ocr", [])
        if not textos: riesgo += 10; causas.append("Sin texto en pantalla")
        mov = esc.get("movimiento", {}).get("intensidad", 1)
        if mov < 0.3: riesgo += 15; causas.append("Escena estática")
        forense.append({"escena": i+1, "inicio": esc.get("inicio_seg"), "duracion": dur,
                        "riesgo_scroll": min(100, riesgo+10),
                        "nivel": "🔴 ALTO" if riesgo>40 else "🟡 MEDIO" if riesgo>20 else "🟢 BAJO",
                        "causas": causas})
    out = f"results/{Path(adn_json).stem}_forensics.json"
    Path(out).write_text(json.dumps({"video": Path(adn_json).stem, "forense": forense}, indent=2))
    print(f"✅ Forense: {out}\n")
    for f in forense:
        bar = "█"*min(10, f["riesgo_scroll"]//10)+"░"*(10-min(10, f["riesgo_scroll"]//10))
        print(f"  Esc {f['escena']:2d} |{bar}| {f['nivel']} | {', '.join(f['causas'])}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("adn"); args = p.parse_args()
    analizar(args.adn)
