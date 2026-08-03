#!/usr/bin/env python3
"""Certificado de autenticidad SHA-256 + verificación."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def firmar(ruta, autor, proyecto):
    ruta = Path(ruta)
    sha = hashlib.sha256()
    with open(ruta,"rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    cert = {"archivo":ruta.name, "autor":autor, "proyecto":proyecto,
            "sha256":sha.hexdigest(), "verificado":True}
    salida = RESULTS_DIR/f"{ruta.stem}_certificado.json"
    guardar_json(str(salida), cert)
    print(f"✅ Certificado: {salida}\n🔑 Hash: {sha.hexdigest()}")
    return cert

def verificar(ruta, cert_path):
    ruta = Path(ruta)
    cert = json.load(open(cert_path))
    sha = hashlib.sha256()
    with open(ruta,"rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    ok = sha.hexdigest() == cert["sha256"]
    print(f"🔍 Verificación: {'✅ AUTÉNTICO' if ok else '❌ MODIFICADO'}")
    return ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("sign")
    p1.add_argument("video"); p1.add_argument("--autor",required=True); p1.add_argument("--proyecto",required=True)
    p2 = sub.add_parser("verify")
    p2.add_argument("video"); p2.add_argument("--certificado",required=True)
    args = parser.parse_args()
    if args.cmd=="sign": firmar(args.video, args.autor, args.proyecto)
    else: verificar(args.video, args.certificado)
