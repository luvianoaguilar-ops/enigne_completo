#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime


def tokenize(t):
    return re.findall(r"\b[\wáéíóúüñÁÉÍÓÚÜÑ'-]+\b", t.lower(), flags=re.UNICODE)


def main():
    if len(sys.argv) < 4:
        print("Uso: format_adapter.py adn.json guion.txt tema output.json")
        sys.exit(1)

    adn = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    guion = Path(sys.argv[2]).read_text(encoding="utf-8")
    tema = sys.argv[3]
    out = sys.argv[4] if len(sys.argv) > 4 else "production_plan.json"

    words = tokenize(guion)
    cursor = 0
    scenes = adn.get("escenas", [])
    bloques = []

    for sc in scenes:
        dur = max(0.1, float(sc.get("duracion_seg", 1)))
        cap = max(1, round(dur * 2.7))
        if sc == scenes[-1]:
            sel = words[cursor:]
        else:
            sel = words[cursor:cursor + cap]
        cursor += len(sel)
        bloques.append(" ".join(sel))

    plan = {
        "schema_version": "1.0",
        "created_at": datetime.now().isoformat(),
        "project": {
            "topic": tema,
            "format": "vertical_9_16",
            "resolution": [1080, 1920]
        },
        "scenes": []
    }

    for i, (sc, b) in enumerate(zip(scenes, bloques)):
        plan["scenes"].append({
            "scene_id": i + 1,
            "duration_sec": sc.get("duracion_seg", 1),
            "voice_text": b,
            "reference_format": {
                "movement_type": sc.get("movimiento", {}).get("tipo", "estático")
            }
        })

    Path(out).write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    print(f"✅ Plan generado: {out}")


if __name__ == "__main__":
    main()
