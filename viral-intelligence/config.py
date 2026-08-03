#!/usr/bin/env python3
"""VIRAL INTELLIGENCE — Unified Configuration."""
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

# Paths
DATA_DIR = BASE_DIR / "data"
DATASET_DIR = DATA_DIR / "dataset"
RESULTS_DIR = BASE_DIR / "results"
TEMP_DIR = BASE_DIR / "data" / "temp"
EXAMPLES_DIR = BASE_DIR / "examples"

# Ensure directories exist
for d in [DATA_DIR, DATASET_DIR, RESULTS_DIR, TEMP_DIR, EXAMPLES_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Analysis settings
FRAME_SAMPLE_RATE = 30
COLOR_THRESHOLD = 30
DEFAULT_FPS = 30.0

# TikTok optimal ranges
TIKTOK_DURACION_OPTIMA = (7, 34)
TIKTOK_BPM_OPTIMO = (110, 145)
TIKTOK_CPM_MINIMO = 14
TIKTOK_GANCHO_MAX = 1.6

# LLM settings
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_TIMEOUT = 120
