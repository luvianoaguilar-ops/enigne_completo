#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OCR temporal mejorado — detección de texto con agrupación por segmentos."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import cv2, pytesseract
from pytesseract import Output, TesseractError
from .utils import RESULTS_DIR, guardar_json

def normalizar_texto(texto: str) -> str:
    texto = texto.lower().strip()
    texto = re.sub(r"\s+", " ", texto)
    return re.sub(r"[^a-záéíóúüñ0-9 ]", "", texto)

def ocr_en_frame(frame, idioma="spa+eng", confianza_minima=45):
    alto_original, ancho_original = frame.shape[:2]
    ancho_objetivo = 960
    escala = ancho_objetivo / ancho_original
    nuevo_alto = int(alto_original * escala)
    frame_grande = cv2.resize(frame, (ancho_objetivo, nuevo_alto), interpolation=cv2.INTER_CUBIC)
    gris = cv2.cvtColor(frame_grande, cv2.COLOR_BGR2GRAY)
    gris = cv2.bilateralFilter(gris, 7, 50, 50)
    try:
        datos = pytesseract.image_to_data(gris, lang=idioma, config="--oem 3 --psm 11", output_type=Output.DICT)
    except TesseractError:
        datos = pytesseract.image_to_data(gris, lang="eng", config="--oem 3 --psm 11", output_type=Output.DICT)

    lineas = {}
    for i, texto in enumerate(datos["text"]):
        texto = texto.strip()
        try: confianza = float(datos["conf"][i])
        except ValueError: confianza = -1
        if not texto or confianza < confianza_minima: continue
        clave = (datos["block_num"][i], datos["par_num"][i], datos["line_num"][i])
        x, y, w, h = int(datos["left"][i]), int(datos["top"][i]), int(datos["width"][i]), int(datos["height"][i])
        if clave not in lineas:
            lineas[clave] = {"palabras": [], "confianzas": [], "x1": x, "y1": y, "x2": x+w, "y2": y+h}
        l = lineas[clave]
        l["palabras"].append(texto); l["confianzas"].append(confianza)
        l["x1"] = min(l["x1"], x); l["y1"] = min(l["y1"], y)
        l["x2"] = max(l["x2"], x+w); l["y2"] = max(l["y2"], y+h)

    resultados = []
    for l in lineas.values():
        txt = " ".join(l["palabras"]).strip()
        if not txt: continue
        resultados.append({
            "texto": txt,
            "confianza": sum(l["confianzas"])/len(l["confianzas"]),
            "x": l["x1"]/ancho_objetivo,
            "y": l["y1"]/nuevo_alto,
            "ancho": (l["x2"]-l["x1"])/ancho_objetivo,
            "alto": (l["y2"]-l["y1"])/nuevo_alto
        })
    return resultados

def agrupar_apariciones(aparecen, intervalo):
    segmentos = {}
    for item in aparecen:
        t_norm = normalizar_texto(item["texto"])
        if len(t_norm) < 2: continue
        segmentos.setdefault(t_norm, [])
        lista = segmentos[t_norm]
        if lista and item["tiempo"] - lista[-1]["fin"] <= intervalo * 1.8:
            c = lista[-1]["_c"]
            lista[-1]["fin"] = item["tiempo"]
            lista[-1]["confianza_media"] = (lista[-1]["confianza_media"]*c + item["confianza"])/(c+1)
            lista[-1]["x"] = (lista[-1]["x"]*c + item["x"])/(c+1)
            lista[-1]["y"] = (lista[-1]["y"]*c + item["y"])/(c+1)
            lista[-1]["ancho"] = (lista[-1]["ancho"]*c + item["ancho"])/(c+1)
            lista[-1]["alto"] = (lista[-1]["alto"]*c + item["alto"])/(c+1)
            lista[-1]["_c"] += 1
        else:
            lista.append({**item, "inicio": item["tiempo"], "fin": item["tiempo"], "_c": 1})
    final = []
    for lista in segmentos.values():
        for s in lista:
            s["apariciones"] = s.pop("_c")
            final.append(s)
    return sorted(final, key=lambda x: x["inicio"])

def analizar_texto_video(ruta_video, intervalo=0.5, idioma="spa+eng"):
    ruta = Path(ruta_video)
    cap = cv2.VideoCapture(str(ruta))
    if not cap.isOpened(): raise RuntimeError(f"No se pudo abrir: {ruta}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_num, siguiente, apariciones, muestras = 0, 0.0, [], 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret: break
            t = frame_num / fps
            if t + 0.0001 >= siguiente:
                for txt in ocr_en_frame(frame, idioma):
                    txt["tiempo"] = t
                    apariciones.append(txt)
                muestras += 1
                siguiente += intervalo
            frame_num += 1
    except pytesseract.TesseractNotFoundError:
        cap.release()
        return {"disponible": False, "error": "Instala: brew install tesseract", "segmentos": []}
    cap.release()
    segmentos = agrupar_apariciones(apariciones, intervalo)
    res = {"disponible": True, "video": ruta.name, "intervalo": intervalo,
           "muestras_ocr": muestras, "segmentos": segmentos}
    salida = RESULTS_DIR / f"{ruta.stem}_ocr.json"
    guardar_json(str(salida), res)
    print(f"✅ OCR guardado: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--intervalo", type=float, default=0.5)
    parser.add_argument("--idioma", default="spa+eng")
    args = parser.parse_args()
    analizar_texto_video(args.video, args.intervalo, args.idioma)
