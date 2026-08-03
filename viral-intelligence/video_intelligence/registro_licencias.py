#!/usr/bin/env python3
"""Registro de licencias y permisos en SQLite."""
from __future__ import annotations
import sqlite3, argparse
from pathlib import Path
DB = Path("results/licencias.db")
DB.parent.mkdir(parents=True, exist_ok=True)

def init():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS activos (
        id INTEGER PRIMARY KEY, nombre TEXT, tipo TEXT, propietario TEXT,
        licencia TEXT, ruta TEXT, consentimiento BOOL, fecha TEXT,
        restricciones TEXT, fuente TEXT, notas TEXT,
        creado TEXT DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit(); conn.close()

def add(nombre, tipo, prop, lic, **kw):
    init()
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO activos (nombre,tipo,propietario,licencia,ruta,consentimiento,fecha,restricciones,fuente,notas) VALUES (?,?,?,?,?,?,?,?,?,?)",
                 (nombre,tipo,prop,lic,kw.get("ruta",""),kw.get("consentimiento",False),
                  kw.get("fecha",""),kw.get("restricciones",""),kw.get("fuente",""),kw.get("notas","")))
    conn.commit(); conn.close()
    print(f"✅ Activo agregado: {nombre}")

def listar():
    init()
    conn = sqlite3.connect(DB); conn.row_factory = sqlite3.Row
    for r in conn.execute("SELECT * FROM activos"):
        print(f"  ID:{r['id']} | {r['nombre']} ({r['tipo']}) | {r['licencia']}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("add")
    p1.add_argument("--nombre",required=True); p1.add_argument("--tipo",required=True)
    p1.add_argument("--propietario",required=True); p1.add_argument("--licencia",required=True)
    p1.add_argument("--ruta",default=""); p1.add_argument("--consentimiento",action="store_true")
    p1.add_argument("--fecha",default=""); p1.add_argument("--restricciones",default="")
    p1.add_argument("--fuente",default=""); p1.add_argument("--notas",default="")
    sub.add_parser("list")
    args = parser.parse_args()
    if args.cmd=="add": add(args.nombre,args.tipo,args.propietario,args.licencia,ruta=args.ruta,
                             consentimiento=args.consentimiento,fecha=args.fecha,
                             restricciones=args.restricciones,fuente=args.fuente,notas=args.notas)
    else: listar()
