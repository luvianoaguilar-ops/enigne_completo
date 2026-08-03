#!/usr/bin/env python3
import sqlite3, json
from pathlib import Path
DB = Path("adn_library.db")
def init():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS adns(id TEXT PRIMARY KEY, url TEXT, dur REAL, cpm REAL, bpm REAL, fecha TEXT)")
    return c
def main():
    c = init()
    for f in Path("dataset").glob("*/adn_video.json"):
        d = json.loads(f.read_text())
        c.execute("INSERT OR REPLACE INTO adns VALUES (?,?,?,?,?,?)",
                  (f.parent.name, d.get("url", ""), d["metadata"]["duracion_segundos"],
                   d.get("estadisticas", {}).get("cortes_por_minuto", 0),
                   d.get("audio", {}).get("bpm", 0), d["fecha_analisis"]))
    c.commit()
    print(f"✅ DB con {len(list(Path('dataset').glob('*/adn_video.json')))} registros")
if __name__ == "__main__": main()
