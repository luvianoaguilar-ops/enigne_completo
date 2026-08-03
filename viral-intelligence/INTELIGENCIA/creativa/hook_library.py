#!/usr/bin/env python3
"""Hook Library — biblioteca de ganchos con tracking de rendimiento."""
from __future__ import annotations
import argparse, json, sqlite3
from pathlib import Path
from datetime import datetime

DB = Path("results/hook_library.db")

def init():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS hooks(
        id INTEGER PRIMARY KEY, texto TEXT UNIQUE, tipo TEXT, 
        emocion TEXT, puntuacion REAL, usos INTEGER, 
        ultimo_uso TEXT, creado TEXT)""")
    conn.commit(); conn.close()

def add(texto: str, tipo: str = "general", emocion: str = "curiosidad"):
    init(); conn = sqlite3.connect(DB)
    conn.execute("INSERT OR REPLACE INTO hooks(texto,tipo,emocion,puntuacion,usos,ultimo_uso,creado) VALUES (?,?,?,?,?,?,?)",
                 (texto, tipo, emocion, 5.0, 0, datetime.now().isoformat(), datetime.now().isoformat()))
    conn.commit(); conn.close()
    print(f"✅ Gancho agregado: {texto[:60]}...")

def rank():
    init(); conn = sqlite3.connect(DB)
    print("🎯 TOP HOOKS:\n")
    for r in conn.execute("SELECT texto, puntuacion, usos, tipo FROM hooks ORDER BY puntuacion DESC LIMIT 20"):
        print(f"  [{r[3]:12}] ⭐{r[1]:.1f} | usos:{r[2]:3d} | {r[0][:80]}")
    conn.close()

def generar(tema: str, cantidad: int = 5):
    plantillas = [
        f"El secreto de {tema} que nadie te cuenta",
        f"Dejá de hacer esto con {tema}",
        f"3 errores que cometés con {tema}",
        f"Cómo {tema} cambió mi vida en 30 días",
        f"Lo que aprendí sobre {tema} después de 100 intentos",
        f"La verdad incómoda sobre {tema}",
        f"Esto es lo que pasa cuando {tema}",
        f"El truco de {tema} que los expertos no quieren que sepas",
        f"Por qué {tema} es más fácil de lo que pensás",
        f"Probé {tema} por una semana y esto pasó",
    ]
    for i, h in enumerate(plantillas[:cantidad], 1):
        print(f"{i}. {h}")
        add(h, tipo="auto", emocion="curiosidad")

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("accion", choices=["add","rank","generar"])
    p.add_argument("--texto","-t"); p.add_argument("--tema"); p.add_argument("--cantidad",type=int,default=5)
    args = p.parse_args()
    if args.accion=="add" and args.texto: add(args.texto)
    elif args.accion=="rank": rank()
    elif args.accion=="generar" and args.tema: generar(args.tema, args.cantidad)
