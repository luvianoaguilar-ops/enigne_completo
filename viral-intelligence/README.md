# 🧬 VIRAL INTELLIGENCE — Unified Production Engine

> **Viral DNA v3.0 × Video Intelligence v1.0**
> **100% GRATIS · 100% LOCAL · macOS Ventura 13.7.8**

---

## 🔥 ¿Qué es esto?

La fusión definitiva de dos proyectos legendarios:

| | **Viral DNA v3.0** | **Video Intelligence v1.0** |
|---|---|---|
| **Archivos** | 9 módulos | 40 módulos |
| **Fortaleza** | Pipeline TikTok directo, score viral simple, Ollama | Análisis técnico profundo, 35+ analizadores, Whisper/OCR/MediaPipe |
| **IA** | Ollama (llama3.2:3b) | Whisper + Tesseract + MediaPipe + KMeans |

**Resultado: 50+ módulos Python, 301+ ideas, 115 prompts, pipeline unificado end-to-end.**

---

## ⚡ Instalación (5 minutos)

```bash
# 1. Dependencias del sistema
brew install ffmpeg python@3.11 tesseract

# 2. Ollama (IA local gratuita)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b

# 3. Python
pip3 install -r requirements.txt

# 4. Verificar
python3 run_pipeline.py --help
```

---

## 🚀 USO RÁPIDO

### Pipeline completo (1 comando)
```bash
python3 run_pipeline.py "URL_DEL_VIDEO" --tema "mi tema"
```

### Solo análisis rápido
```bash
python3 run_pipeline.py "video.mp4" --tema "cocina" --fast
```

### Solo analizar sin generar
```bash
python3 run_pipeline.py "URL" --tema "finanzas" --analyze
```

### Con guion personalizado
```bash
python3 run_pipeline.py "video.mp4" --tema "productividad" --guion mi_guion.txt
```

---

## 🔧 MÓDULOS DISPONIBLES

### CORE (herencia A)
```bash
python3 CORE/viral_scanner.py "URL"          # Escanear video completo
python3 CORE/viral_score_original.py ADN.json # Score viral clásico
```

### PRODUCCION (herencia A)
```bash
python3 PRODUCCION/format_adapter.py ADN.json guion.txt "tema"     # ADN → plan
python3 PRODUCCION/render_free.py plan.json output.mp4              # Renderizar
```

### UTILS (herencia A)
```bash
python3 UTILS/ai_local.py "Tu prompt"                               # IA local
```

### video_intelligence/ (herencia B)
```bash
python -m video_intelligence.analyzer_v2 video.mp4                  # Análisis profundo
python -m video_intelligence.tiktok_hook_analyzer video.mp4        # Hook TikTok
python -m video_intelligence.mapa_energia video.mp4                 # Mapa energía
python -m video_intelligence.movimiento_camara video.mp4            # Cámara
python -m video_intelligence.texto_ocr video.mp4                    # OCR
python -m video_intelligence.local_color_palette video.mp4          # Paleta
python -m video_intelligence.auto_crop_vertical video.mp4           # Crop vertical
python -m video_intelligence.silence_cutter video.mp4               # Cortar silencios
python -m video_intelligence.loop_validator video.mp4               # Validar loop
python -m video_intelligence.batch_adn_sqlite stats                 # Biblioteca
python -m video_intelligence.cli_dashboard "video"                  # Dashboard
python -m video_intelligence.linea_tiempo --reporte R --ocr O --energia E --camara C  # Timeline
python -m video_intelligence.estimador_planos video.mp4             # Tipos plano
python -m video_intelligence.separador_stems video.mp4              # Stems audio
python -m video_intelligence.salient_maps video.mp4                 # Saliencia
python -m video_intelligence.limpiador_audio video.mp4              # Limpiar audio
python -m video_intelligence.local_script_pacing guion.txt          # Ritmo guion
python -m video_intelligence.prompt_engine reporte.json --concepto "tema"  # Prompts
python -m video_intelligence.seo_metadata reporte.json --concepto "tema"   # SEO
python -m video_intelligence.watermark_invisible sign video.mp4 --autor "yo" --proyecto "x"  # Certificar
python -m video_intelligence.registro_licencias add --nombre "x" --tipo "video" --propietario "yo" --licencia "CC"
python -m video_intelligence.detector_duplicados scan --carpeta data/
python -m video_intelligence.generador_storyboard video.mp4 --reporte R --ocr O --planos P --camara C
python -m video_intelligence.exportador_resolve_csv video.mp4 --reporte R --timeline T
python -m video_intelligence.laboratorio_ab reporte.json --tipo hook
```

---

## 📁 ESTRUCTURA

```
viral-intelligence/
├── run_pipeline.py              ← 🆕 Pipeline unificado A+B
├── CORE/                        ← Asistente A original
│   ├── viral_scanner.py         # Descarga + metadatos + escenas + audio + OCR + movimiento
│   ├── hook_analyzer_original.py
│   └── viral_score_original.py
├── PRODUCCION/                  ← Asistente A
│   ├── format_adapter.py        # ADN → plan de producción
│   └── render_free.py           # Renderizador FFmpeg
├── UTILS/                       ← Asistente A
│   └── ai_local.py              # Cliente Ollama
├── SCRIPTS/
│   └── menu.sh                  # Menú interactivo
├── video_intelligence/          ← Asistente B (40 módulos)
│   ├── analyzer_v2.py           # Análisis técnico profundo
│   ├── tiktok_*.py              # 5 módulos TikTok
│   ├── auto_crop_vertical.py    # Transformación
│   ├── mapa_energia.py          # Energía audiovisual
│   ├── movimiento_camara.py     # Optical flow + affine
│   ├── texto_ocr.py             # OCR con agrupación
│   ├── linea_tiempo.py          # Timeline CSV/JSON
│   ├── estimador_planos.py      # MediaPipe 13 tipos
│   ├── salient_maps.py          # Mapas de atención
│   └── ...                      # 25+ módulos más
├── docs/
│   ├── IDEAS_UNIFICADAS.md      ← 🆕 301+ ideas (A+B+nuevas)
│   ├── PROMPT_BOOK_UNIFICADO.md ← 🆕 115 prompts (A+B)
│   └── GUIA_FUSION.md           ← Guía de migración
├── data/                        # Datos y proyectos
├── results/                     # Resultados de análisis
├── examples/                    # Ejemplos
└── requirements.txt
```

---

## 💸 STACK 100% GRATIS

| Función | Herramienta | Costo |
|---|---|---|
| Cerebro IA | Ollama (Llama 3.2) | $0 |
| Transcripción | Whisper local | $0 |
| OCR | Tesseract | $0 |
| Voz | macOS `say` / Piper | $0 |
| Video | FFmpeg | $0 |
| Base datos | SQLite | $0 |
| Dashboard | HTML5 + Canvas | $0 |
| **TOTAL** | | **$0/mes** |

---

## 📊 MÉTRICAS UNIFICADAS

| Métrica | Fuente | Peso |
|---|---|---|
| Duración (7-34s óptimo) | A | 15% |
| CPM (cortes por minuto) | A | 15% |
| Gancho (<1.6s) | A | 10% |
| BPM (110-145 óptimo) | A | 10% |
| Hook Score (0-100) | B | 15% |
| Sound Score (0-100) | B | 15% |
| Retención (drop-off 3s) | B | 10% |
| Formato (9:16 + FPS) | B | 10% |

---

## 📚 DOCUMENTACIÓN

- `docs/IDEAS_UNIFICADAS.md` → 301+ ideas en 14 tiers
- `docs/PROMPT_BOOK_UNIFICADO.md` → 115 prompts en 11 categorías
- `docs/GUIA_FUSION.md` → Cómo migrar de A o B al sistema unificado

---

*Fusión construida con ❤️ por Viral DNA v3.0 + Video Intelligence v1.0 + 55+ ideas nuevas*
*Versión: Unified 1.0 | macOS Ventura 13.7.8 | $0 costo total*
