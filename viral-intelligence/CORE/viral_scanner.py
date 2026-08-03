#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIRAL SCANNER v3.0
Uso: python3 CORE/viral_scanner.py "URL"
"""
import os, sys, json, subprocess, shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATASET_DIR = BASE_DIR / "dataset"
TEMP_DIR = BASE_DIR / "temp"

class ViralScanner:
    def __init__(self, url):
        self.url = url
        self.video_path = None
        self.video_id = None
        self.report = {
            "url": url,
            "fecha_analisis": datetime.now().isoformat(),
            "metadata": {},
            "escenas": [],
            "audio": {},
            "estadisticas": {}
        }

    def descargar(self):
        TEMP_DIR.mkdir(exist_ok=True)
        cmd = ["yt-dlp", "-f", "best[height<=1080]/best", "-o", str(TEMP_DIR / "%(id)s.%(ext)s"), "--no-playlist", self.url]
        subprocess.run(cmd, check=True, capture_output=True)
        archivos = [f for f in TEMP_DIR.iterdir() if f.suffix in (".mp4", ".webm", ".mkv", ".mov")]
        if not archivos:
            raise Exception("No se pudo descargar")
        self.video_path = max(archivos, key=os.path.getctime)
        self.video_id = self.video_path.stem
        return self

    def extraer_metadata(self):
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", str(self.video_path)]
        data = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
        vs = next(s for s in data["streams"] if s["codec_type"] == "video")
        num, den = vs["r_frame_rate"].split("/")
        self.report["metadata"] = {
            "resolucion": f"{vs['width']}x{vs['height']}",
            "fps": round(int(num) / int(den), 2),
            "duracion_segundos": round(float(data["format"]["duration"]), 2)
        }
        return self

    def detectar_escenas(self):
        from scenedetect import detect, ContentDetector
        for i, (inicio, fin) in enumerate(detect(str(self.video_path), ContentDetector(threshold=27.0))):
            self.report["escenas"].append({
                "escena": i + 1,
                "inicio_seg": round(inicio.get_seconds(), 2),
                "fin_seg": round(fin.get_seconds(), 2),
                "duracion_seg": round(fin.get_seconds() - inicio.get_seconds(), 2),
                "frame_inicio": inicio.get_frames(),
                "frame_fin": fin.get_frames()
            })
        return self

    def guardar_reporte(self):
        salida = DATASET_DIR / self.video_id
        salida.mkdir(parents=True, exist_ok=True)
        with open(salida / "adn_video.json", "w", encoding="utf-8") as f:
            json.dump(self.report, f, indent=2, ensure_ascii=False)
        return self

    def limpiar(self):
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR)


def main():
    if len(sys.argv) < 2:
        print('Uso: python3 CORE/viral_scanner.py "URL"')
        sys.exit(1)
    s = ViralScanner(sys.argv[1])
    try:
        s.descargar().extraer_metadata().detectar_escenas().guardar_reporte()
    finally:
        s.limpiar()


if __name__ == "__main__":
    main()
