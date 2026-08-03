#!/usr/bin/env python3
"""Knowledge Base Builder — FAQ automático desde preguntas recurrentes."""
from __future__ import annotations
import argparse, json, re, sqlite3
from pathlib import Path
from collections import Counter

DB = Path("results/knowledge_base.db")

def init():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS faq(
        id INTEGER PRIMARY KEY, pregunta TEXT UNIQUE, categoria TEXT,
        respuestas TEXT, frecuencia INTEGER, ultima_vez TEXT)""")
    conn.commit(); conn.close()

def extraer_preguntas(comentarios: list) -> list:
    preguntas = []
    for c in comentarios:
        if "?" in c and len(c) > 10:
            limpia = re.sub(r'[^\wáéíóúüñ\s?]', '', c.lower()).strip()
            preguntas.append(limpia)
    return [p for p, n in Counter(preguntas).most_common(20)]

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("accion", choices=["build","show"])
    p.add_argument("--comentarios", help="JSON con lista de comentarios")
    args = p.parse_args()
    init()
    if args.accion=="build" and args.comentarios:
        comentarios = json.loads(Path(args.comentarios).read_text()) if Path(args.comentarios).exists() else json.loads(args.comentarios)
        preguntas = extraer_preguntas(comentarios if isinstance(comentarios, list) else comentarios.get("comentarios",[]))
        conn = sqlite3.connect(DB)
        for p in preguntas:
            conn.execute("INSERT OR IGNORE INTO faq(pregunta,frecuencia,ultima_vez) VALUES (?,1,datetime('now'))", (p,))
        conn.commit(); conn.close()
        print(f"✅ {len(preguntas)} preguntas extraídas\n")
        for i, p in enumerate(preguntas[:10], 1): print(f"  {i}. {p}")
    else:
        conn = sqlite3.connect(DB)
        print("\n📚 BASE DE CONOCIMIENTO:\n")
        for r in conn.execute("SELECT pregunta, frecuencia FROM faq ORDER BY frecuencia DESC LIMIT 20"):
            print(f"  ❓ {r[0][:80]} ({r[1]}x)")
        conn.close()
