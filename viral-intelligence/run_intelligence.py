#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════════╗
║  🧠 VIRAL INTELLIGENCE — Master Intelligence Runner              ║
║  Ejecuta TODOS los módulos de INTELIGENCIA en orden              ║
║  Uso: python3 run_intelligence.py --tema "mi tema" --video VID   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations
import argparse, json, sys, subprocess
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
INTEL = BASE / "INTELIGENCIA"

MODULOS = {
    # TIER 11: Creativa
    "script_doctor":       (INTEL/"creativa/script_doctor.py",        "Análisis y mejora de guiones"),
    "hook_library":        (INTEL/"creativa/hook_library.py",          "Biblioteca de ganchos con ranking"),
    "series_architect":    (INTEL/"creativa/series_architect.py",      "Diseñador de series de 10+ partes"),
    "emotion_arc":         (INTEL/"creativa/emotion_arc_designer.py",  "Curva emocional segundo a segundo"),
    "voice_energy":        (INTEL/"creativa/voice_energy_calibrator.py","Calibrador de energía vocal"),

    # TIER 12: Autónoma
    "content_recycler":    (INTEL/"autonoma/content_recycler.py",      "Re-empaquetado de contenido viejo"),
    "chapter_marker":      (INTEL/"autonoma/chapter_marker.py",        "Detección automática de capítulos"),
    "content_versioning":  (INTEL/"autonoma/content_versioning.py",    "Git para videos (commit/log)"),
    "multiformat_export":  (INTEL/"autonoma/multiformat_export.py",    "Exportación multi-formato"),
    "batch_processor":     (INTEL/"autonoma/batch_processor.py",       "Procesador por lotes"),
    "content_bank":        (INTEL/"autonoma/content_bank.py",          "Banco de contenido 90 días"),
    "repurpose_chain":     (INTEL/"autonoma/repurpose_chain.py",       "Cadena de repurposing"),
    "loop_seam":           (INTEL/"autonoma/loop_seam_detector.py",    "Detector de loop perfecto"),

    # TIER 13: Analytics
    "persona_generator":   (INTEL/"analytics/persona_generator.py",    "Generador de personas de audiencia"),
    "dropoff_forensics":   (INTEL/"analytics/dropoff_forensics.py",    "Análisis forense de drop-off"),
    "competitor_dna":      (INTEL/"analytics/competitor_dna.py",       "Base de datos de competidores"),
    "content_health":      (INTEL/"analytics/content_health.py",       "Dashboard de salud de contenido"),
    "best_time_poster":    (INTEL/"analytics/best_time_poster.py",     "Calculador de mejor hora"),
    "ab_test_lab":         (INTEL/"analytics/ab_test_lab.py",          "Laboratorio A/B testing"),
    "viral_simulator":     (INTEL/"analytics/viral_simulator.py",      "Simulador de trayectoria viral"),
    "content_gap_finder":  (INTEL/"analytics/content_gap_finder.py",   "Detector de gaps de contenido"),

    # TIER 14: Ecosistema
    "community_cocreator": (INTEL/"ecosistema/community_cocreator.py", "Co-creación con la comunidad"),
    "collab_radar":        (INTEL/"ecosistema/collab_radar.py",        "Radar de colaboraciones"),
    "knowledge_base":      (INTEL/"ecosistema/knowledge_base.py",      "Base de conocimiento FAQ"),
    "hashtag_optimizer":   (INTEL/"ecosistema/hashtag_optimizer.py",   "Optimizador de hashtags"),
}


def ejecutar_modulo(nombre: str, info: tuple, args_extra: list = None) -> bool:
    path, desc = info
    if not path.exists(): return False
    print(f"\n{'─'*60}")
    print(f"  {desc}")
    print(f"{'─'*60}")
    cmd = [sys.executable, str(path)]
    if args_extra: cmd.extend(args_extra)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, cwd=str(BASE))
        print(r.stdout[-500:] if len(r.stdout) > 500 else r.stdout)
        if r.stderr: print(f"  ⚠️ {r.stderr[-200:]}")
        return r.returncode == 0
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="🧠 VIRAL INTELLIGENCE — Master Runner")
    parser.add_argument("--tema", required=True, help="Tema principal")
    parser.add_argument("--video", help="Ruta a video para análisis")
    parser.add_argument("--guion", help="Ruta a guion (.txt)")
    parser.add_argument("--nicho", help="Nicho de contenido (default: del tema)")
    parser.add_argument("--fast", action="store_true", help="Solo módulos rápidos")
    parser.add_argument("--all", action="store_true", help="Ejecutar TODOS")
    args = parser.parse_args()

    tema = args.tema
    nicho = args.nicho or tema.split()[0].lower()
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║       🧠 VIRAL INTELLIGENCE — INTELIGENCIA CREATIVA      ║
║   Tema: {tema:<47} ║
║   Nicho: {nicho:<46} ║
╚═══════════════════════════════════════════════════════════╝
""")
    resultados = {}
    start = datetime.now()

    # ── TIER 11: Creativa ──
    print("\n🎨 TIER 11: INTELIGENCIA CREATIVA")
    if args.guion and Path(args.guion).exists():
        resultados["script_doctor"] = ejecutar_modulo("script_doctor", MODULOS["script_doctor"], [args.guion])
    resultados["hook_library"] = ejecutar_modulo("hook_library", MODULOS["hook_library"], ["generar", "--tema", tema])
    resultados["series_architect"] = ejecutar_modulo("series_architect", MODULOS["series_architect"], [tema])
    resultados["emotion_arc"] = ejecutar_modulo("emotion_arc", MODULOS["emotion_arc"], [])
    if args.guion and Path(args.guion).exists():
        resultados["voice_energy"] = ejecutar_modulo("voice_energy", MODULOS["voice_energy"], [args.guion])

    # ── TIER 12: Autónoma ──
    print("\n🤖 TIER 12: CONTENIDO AUTÓNOMO")
    if not args.fast:
        resultados["content_recycler"] = ejecutar_modulo("content_recycler", MODULOS["content_recycler"], ["--tema", tema])
        resultados["content_bank"] = ejecutar_modulo("content_bank", MODULOS["content_bank"], [tema])
        resultados["repurpose_chain"] = ejecutar_modulo("repurpose_chain", MODULOS["repurpose_chain"], [tema])
    resultados["content_versioning"] = ejecutar_modulo("content_versioning", MODULOS["content_versioning"], ["log"])
    if args.video:
        resultados["chapter_marker"] = ejecutar_modulo("chapter_marker", MODULOS["chapter_marker"], [args.video])
        resultados["multiformat_export"] = ejecutar_modulo("multiformat_export", MODULOS["multiformat_export"], [args.video])
        resultados["loop_seam"] = ejecutar_modulo("loop_seam", MODULOS["loop_seam"], [args.video])

    # ── TIER 13: Analytics ──
    print("\n📊 TIER 13: ANALYTICS AVANZADO")
    resultados["persona_generator"] = ejecutar_modulo("persona_generator", MODULOS["persona_generator"], [nicho])
    resultados["best_time_poster"] = ejecutar_modulo("best_time_poster", MODULOS["best_time_poster"], [nicho])
    resultados["content_gap_finder"] = ejecutar_modulo("content_gap_finder", MODULOS["content_gap_finder"], ["--nicho", nicho])
    resultados["content_health"] = ejecutar_modulo("content_health", MODULOS["content_health"], [])
    resultados["ab_test_lab"] = ejecutar_modulo("ab_test_lab", MODULOS["ab_test_lab"], [])
    if not args.fast:
        resultados["viral_simulator"] = ejecutar_modulo("viral_simulator", MODULOS["viral_simulator"], ["50"])
        resultados["competitor_dna"] = ejecutar_modulo("competitor_dna", MODULOS["competitor_dna"], ["compare"])

    # ── TIER 14: Ecosistema ──
    print("\n🌐 TIER 14: ECOSISTEMA & COMUNIDAD")
    resultados["community_cocreator"] = ejecutar_modulo("community_cocreator", MODULOS["community_cocreator"], [tema])
    resultados["collab_radar"] = ejecutar_modulo("collab_radar", MODULOS["collab_radar"], ["--nicho", nicho])
    resultados["hashtag_optimizer"] = ejecutar_modulo("hashtag_optimizer", MODULOS["hashtag_optimizer"], [nicho])
    resultados["knowledge_base"] = ejecutar_modulo("knowledge_base", MODULOS["knowledge_base"], ["show"])

    # ── Summary ──
    elapsed = (datetime.now() - start).total_seconds()
    ok = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║              🧠 INTELIGENCIA COMPLETADA                   ║
╠═══════════════════════════════════════════════════════════╣
║  ✅ {ok}/{total} módulos ejecutados correctamente
║  ⏱️  Tiempo: {elapsed:.1f}s
║  📁 Resultados en: results/
║  📚 Docs: docs/IDEAS_UNIFICADAS.md (301+ ideas)
║  📖 Prompts: docs/PROMPT_BOOK_UNIFICADO.md (115 prompts)
╚═══════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
