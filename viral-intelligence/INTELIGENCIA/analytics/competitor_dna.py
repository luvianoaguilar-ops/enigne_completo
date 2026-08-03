#!/usr/bin/env python3
"""Competitor DNA Database — base de datos de ADN de competidores."""
from __future__ import annotations
import argparse, json, sqlite3
from pathlib import Path
from datetime import datetime

DB = Path("results/competitors.db")

def init():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS competitors(
        id INTEGER PRIMARY KEY, nombre TEXT, nicho TEXT, plataforma TEXT,
        seguidores INTEGER, videos_analizados INTEGER, cpm_prom REAL,
        bpm_prom REAL, hook_score_prom REAL, virality_prom REAL,
        ultima_actualizacion TEXT)""")
    conn.commit(); conn.close()

def add(nombre: str, nicho: str, **kw):
    init(); conn = sqlite3.connect(DB)
    conn.execute("INSERT OR REPLACE INTO competitors(nombre,nicho,plataforma,seguidores,videos_analizados,cpm_prom,bpm_prom,hook_score_prom,virality_prom,ultima_actualizacion) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (nombre, nicho, kw.get("plataforma","TikTok"), kw.get("seguidores",0),
         kw.get("videos",0), kw.get("cpm",0), kw.get("bpm",0),
         kw.get("hook",0), kw.get("virality",0), datetime.now().isoformat()))
    conn.commit(); conn.close()
    print(f"✅ Competidor agregado: {nombre}")

def compare():
    init(); conn = sqlite3.connect(DB)
    print("\n📊 RANKING DE COMPETIDORES:\n")
    print(f"{'Nombre':20} | {'Nicho':15} | {'CPM':>6} | {'BPM':>6} | {'Hook':>5} | {'Virality':>8}")
    print("-"*75)
    for r in conn.execute("SELECT nombre, nicho, cpm_prom, bpm_prom, hook_score_prom, virality_prom FROM competitors ORDER BY virality_prom DESC"):
        print(f"{r[0]:20} | {r[1]:15} | {r[2]:6.1f} | {r[3]:6.1f} | {r[4]:5.0f} | {r[5]:8.0f}")
    conn.close()

if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("accion", choices=["add","compare"])
    p.add_argument("--nombre"); p.add_argument("--nicho"); p.add_argument("--cpm",type=float,default=0)
    p.add_argument("--bpm",type=float,default=0); p.add_argument("--hook",type=float,default=0)
    p.add_argument("--virality",type=float,default=0); p.add_argument("--seguidores",type=int,default=0)
    args = p.parse_args()
    if args.accion=="add" and args.nombre: add(args.nombre, args.nicho or "general", cpm=args.cpm, bpm=args.bpm, hook=args.hook, virality=args.virality, seguidores=args.seguidores)
    else: compare()
