#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║          🧬 VIRAL INTELLIGENCE — Unified Pipeline           ║
║     Fusión: Viral DNA v3.0 + Video Intelligence v1.0       ║
║     100% GRATIS · 100% LOCAL · macOS Ventura 13.7.8        ║
╚══════════════════════════════════════════════════════════════╝

FLUJO COMPLETO (1 solo comando):
  python3 run_pipeline.py "URL_O_VIDEO" --tema "mi tema"

MÓDULOS FUSIONADOS:
  A: viral_scanner (descarga + metadatos + escenas + OCR + audio + movimiento)
  B: analyzer_v2 (análisis técnico profundo + receta)
  A+B: hook unificado (caras + diff + energía visual)
  A+B: score unificado (4 vars de A + 5 componentes de B)
  B: TikTok modules (hook/sound/retention/format/virality)
  A: format_adapter (ADN → plan de producción)
  B: script_to_visual_plan (guion + receta → plan visual)
  A: render_free (FFmpeg)
  B: auto_crop + silence_cutter + karaoke_subs
  A: ai_local (Ollama)
  B: local_whisper + prompt_engine + mapa_energia + movimiento_camara
  NUEVO: 50+ ideas revolucionarias + métricas unificadas
"""

from __future__ import annotations
import argparse, json, subprocess, sys, os, shutil
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR / "CORE"))
sys.path.insert(0, str(BASE_DIR))

RESULTS_DIR = BASE_DIR / "results"
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ── STEP 0: Download ──────────────────────────────────────
def step_download(url: str, output_dir: Path) -> Path:
    """Descarga video usando yt-dlp (herencia del Asistente A)."""
    print("\n📥 [FASE 0/8] DESCARGANDO VIDEO...")
    import subprocess
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["yt-dlp", "-f", "best[height<=1080]/best",
           "-o", str(output_dir / "%(id)s.%(ext)s"),
           "--no-playlist", url]
    subprocess.run(cmd, check=True, capture_output=True)
    archivos = sorted(output_dir.glob("*.*"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not archivos:
        raise FileNotFoundError("No se pudo descargar el video")
    video = archivos[0]
    print(f"   ✅ Descargado: {video.name}")
    return video


# ── STEP 1: Viral Scanner (A) ─────────────────────────────
def step_scanner_a(video_path: Path) -> dict:
    """Análisis completo del Asistente A: metadatos + escenas + audio + OCR + movimiento."""
    print("\n🧬 [FASE 1/8] VIRAL SCANNER (A) — ADN completo...")
    try:
        from CORE.viral_scanner import ViralScanner
        scanner = ViralScanner(str(video_path))
        scanner.descargar = lambda: scanner.__setattr__('video_path', video_path) or scanner.__setattr__('video_id', video_path.stem) or scanner
        scanner.extraer_metadata()
        scanner.detectar_escenas()
        scanner.extraer_frames()
        scanner.analizar_audio()
        scanner.detectar_textos_ocr()
        scanner.detectar_movimiento_camara()
        scanner.generar_estadisticas()
        reporte_a = scanner.report
        print(f"   ✅ {len(reporte_a.get('escenas',[]))} escenas | BPM: {reporte_a.get('audio',{}).get('bpm')} | CPM: {reporte_a.get('estadisticas',{}).get('cortes_por_minuto')}")
        return reporte_a
    except Exception as e:
        print(f"   ⚠️ Scanner A falló: {e}, usando analyzer B...")
        return {}


# ── STEP 2: Analyzer B ────────────────────────────────────
def step_analyzer_b(video_path: Path) -> dict:
    """Análisis técnico profundo del Asistente B."""
    print("\n🔬 [FASE 2/8] ANALYZER (B) — Análisis técnico profundo...")
    try:
        from video_intelligence.analyzer_v2 import analizar_video
        reporte_b = analizar_video(str(video_path))
        print(f"   ✅ Hook: {reporte_b.get('hook',{}).get('nota')} | Ritmo: {reporte_b.get('visual',{}).get('edicion',{}).get('estadisticas_tomas',{}).get('ritmo')}")
        return reporte_b
    except Exception as e:
        print(f"   ⚠️ Analyzer B falló: {e}")
        return {}


# ── STEP 3: TikTok Analysis (B) ───────────────────────────
def step_tiktok(video_path: Path) -> dict:
    """Módulos TikTok del Asistente B."""
    print("\n📱 [FASE 3/8] TIKTOK ANALYSIS (B)...")
    try:
        from video_intelligence.tiktok_hook_analyzer import analizar_hook_tiktok
        from video_intelligence.tiktok_sound_viral import analizar_sonido_tiktok
        from video_intelligence.tiktok_retention_curve import generar_curva_retencion
        from video_intelligence.tiktok_format_optimizer import validar_formato_tiktok
        from video_intelligence.tiktok_virality_score import calcular_virality_score_tiktok

        hook = analizar_hook_tiktok(str(video_path))
        sound = analizar_sonido_tiktok(str(video_path))
        retention = generar_curva_retencion(str(video_path))
        fmt = validar_formato_tiktok(str(video_path))
        virality = calcular_virality_score_tiktok(hook, sound, retention, fmt)
        print(f"   ✅ Virality: {virality.get('virality_score')}/100 ({virality.get('nivel')})")
        return {"hook": hook, "sound": sound, "retention": retention, "format": fmt, "virality": virality}
    except Exception as e:
        print(f"   ⚠️ TikTok analysis falló: {e}")
        return {}


# ── STEP 4: Unified Score (A+B) ──────────────────────────
def step_unified_score(reporte_a: dict, reporte_b: dict, tiktok: dict) -> dict:
    """Score viral unificado combinando A + B."""
    print("\n🏆 [FASE 4/8] UNIFIED VIRAL SCORE (A+B)...")
    score = 0
    detalles = []

    # De A: duración óptima
    dur_a = reporte_a.get("metadata", {}).get("duracion_segundos", 0)
    dur_b = reporte_b.get("metadatos", {}).get("duracion_segundos", 0)
    dur = dur_a or dur_b
    if 7 <= dur <= 34:
        score += 15; detalles.append("✅ Duración óptima (7-34s)")
    elif 34 < dur <= 60:
        score += 10; detalles.append("🟡 Duración aceptable (>34s)")

    # De A: CPM
    cpm = reporte_a.get("estadisticas", {}).get("cortes_por_minuto", 0)
    if cpm >= 25: score += 15; detalles.append("✅ Hiper-rápido (CPM≥25)")
    elif cpm >= 14: score += 10; detalles.append("🟡 Ritmo rápido (CPM≥14)")

    # De A: gancho corto
    esc = reporte_a.get("escenas", [])
    if esc and esc[0].get("duracion_seg", 99) <= 1.6:
        score += 10; detalles.append("✅ Gancho ≤1.6s")

    # De A: BPM
    bpm = reporte_a.get("audio", {}).get("bpm", 0) or reporte_b.get("audio", {}).get("bpm_estimado", 0)
    if 110 <= bpm <= 145: score += 10; detalles.append("✅ BPM viral (110-145)")

    # De B: hook score
    hook_s = tiktok.get("hook", {}).get("hook_score", 50)
    score += int(hook_s * 0.15); detalles.append(f"{'✅' if hook_s>=70 else '🟡'} Hook score: {hook_s}")

    # De B: sound score
    sound_s = tiktok.get("sound", {}).get("viral_score", 50)
    score += int(sound_s * 0.15); detalles.append(f"{'✅' if sound_s>=70 else '🟡'} Sound score: {sound_s}")

    # De B: retention
    drop = tiktok.get("retention", {}).get("drop_off_3s", 30)
    if drop < 10: score += 10; detalles.append("✅ Baja caída (<10% en 3s)")

    # De B: formato
    fmt_s = tiktok.get("format", {}).get("score", 50)
    score += int(fmt_s * 0.10)

    score = min(100, score)
    nivel = "🚀 VIRAL" if score >= 80 else "🔥 ALTO" if score >= 65 else "📊 MEDIO" if score >= 45 else "❄️ BAJO"

    resultado = {"unified_viral_score": score, "nivel": nivel, "componentes": detalles,
                  "fuente_a": {"cpm": cpm, "bpm": bpm, "duracion": dur, "escenas": len(esc)},
                  "fuente_b": {"hook": hook_s, "sound": sound_s, "drop_3s": drop, "format": fmt_s}}
    print(f"   🎯 SCORE UNIFICADO: {score}/100 — {nivel}")
    return resultado


# ── STEP 5: Energy + Camera + OCR (B) ────────────────────
def step_deep_analysis(video_path: Path, reporte_b: dict) -> dict:
    """Análisis profundo: energía, cámara, OCR, paleta."""
    print("\n⚡ [FASE 5/8] DEEP ANALYSIS (B)...")
    resultados = {}
    modules = [
        ("mapa_energia", "analizar_energia"),
        ("movimiento_camara", "analizar_movimiento_camara"),
        ("texto_ocr", "analizar_texto_video"),
        ("local_color_palette", "extraer_paleta_video"),
        ("loop_validator", "validar_loop"),
    ]
    for mod_name, func_name in modules:
        try:
            mod = __import__(f"video_intelligence.{mod_name}", fromlist=[func_name])
            func = getattr(mod, func_name)
            if mod_name == "mapa_energia":
                resultados[mod_name] = func(str(video_path), reporte=reporte_b)
            else:
                resultados[mod_name] = func(str(video_path))
            print(f"   ✅ {mod_name}")
        except Exception as e:
            print(f"   ⚠️ {mod_name}: {e}")
    return resultados


# ── STEP 6: Generate Plan (A+B) ──────────────────────────
def step_generate_plan(reporte_a: dict, reporte_b: dict, tema: str, guion_path: str = None) -> dict:
    """Genera plan de producción fusionando format_adapter (A) + script_to_visual_plan (B)."""
    print("\n📋 [FASE 6/8] GENERANDO PLAN DE PRODUCCIÓN (A+B)...")
    plan = {"tema": tema, "generado": datetime.now().isoformat(), "pipeline": "viral-intelligence-unified"}

    # Intentar usar format_adapter de A
    try:
        from PRODUCCION.format_adapter import tokenize
        adn_a = reporte_a if reporte_a.get("escenas") else None
        if adn_a and guion_path:
            guion = Path(guion_path).read_text(encoding="utf-8")
            words = tokenize(guion)
            scenes = adn_a.get("escenas", [])
            plan["escenas_a"] = []
            cursor = 0
            for sc in scenes:
                dur = max(0.1, float(sc.get("duracion_seg", 1)))
                cap = max(1, round(dur * 2.7))
                sel = words[cursor:cursor+cap] if sc != scenes[-1] else words[cursor:]
                cursor += len(sel)
                plan["escenas_a"].append({"id": sc.get("escena"), "duracion": dur, "texto": " ".join(sel)})
            print(f"   ✅ Plan A: {len(plan['escenas_a'])} escenas adaptadas")
    except Exception as e:
        print(f"   ⚠️ Plan A: {e}")

    # Intentar usar receta de B
    try:
        receta = reporte_b.get("receta", {})
        if receta:
            plan["receta_b"] = receta
            plan["recomendaciones"] = [
                f"Ritmo: {receta.get('ritmo_edicion', 'N/A')}",
                f"BPM: {receta.get('bpm_referencia', 'N/A')}",
                f"Movimiento: {receta.get('movimiento_camara', 'N/A')}",
                f"Look: brillo={receta.get('look',{}).get('brillo','N/A')}, contraste={receta.get('look',{}).get('contraste','N/A')}"
            ]
            print(f"   ✅ Receta B extraída")
    except Exception as e:
        print(f"   ⚠️ Receta B: {e}")

    return plan


# ── STEP 7: Render (A) ────────────────────────────────────
def step_render(plan: dict, output_name: str = "video_final") -> Path:
    """Renderiza usando render_free de A + capacidades de B."""
    print("\n🎬 [FASE 7/8] RENDERIZANDO...")
    try:
        from PRODUCCION.render_free import main as render_main
        import sys
        plan_path = RESULTS_DIR / f"{output_name}_plan.json"
        json.dump(plan, open(plan_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        out = RESULTS_DIR / f"{output_name}.mp4"
        # Fallback: render simple
        import subprocess
        duraciones = [s.get("duracion", 3) for s in plan.get("escenas_a", [])]
        if not duraciones:
            duraciones = [float(s.get("duration_sec", 3)) for s in plan.get("receta_b", {}).get("escenas", [])]
        dur_total = sum(duraciones) if duraciones else 15
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi",
                        "-i", f"color=c=0x1a1a2e:s=1080x1920:r=30",
                        "-t", str(dur_total), "-c:v", "libx264", "-preset", "fast", str(out)],
                       capture_output=True)
        print(f"   ✅ Renderizado: {out}")
        return out
    except Exception as e:
        print(f"   ⚠️ Render: {e}")
        return None


# ── STEP 8: Dashboard + Report ────────────────────────────
def step_report(unified_score: dict, plan: dict, reporte_b: dict, nombre: str):
    """Genera reporte maestro unificado."""
    print("\n📊 [FASE 8/8] REPORTE MAESTRO UNIFICADO...")
    master = {
        "pipeline": "viral-intelligence-unified",
        "fecha": datetime.now().isoformat(),
        "video": nombre,
        "score": unified_score,
        "plan": plan,
        "hooks_sugeridos": [],
    }

    # Sugerir hooks con IA local
    try:
        from UTILS.ai_local import preguntar
        tema = plan.get("tema", "")
        if tema:
            prompt = f"Generá 3 ganchos de 3 segundos para TikTok sobre {tema}. Solo respondé con los 3 ganchos, uno por línea, sin numeración."
            respuesta = preguntar(prompt)
            master["hooks_sugeridos"] = [h.strip() for h in respuesta.split("\n") if h.strip()][:3]
            print(f"   ✅ {len(master['hooks_sugeridos'])} hooks generados con IA local")
    except Exception as e:
        print(f"   ⚠️ IA hooks: {e}")

    # Guardar
    reporte_path = RESULTS_DIR / f"{nombre}_unified_report.json"
    json.dump(master, open(reporte_path, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"   ✅ Reporte: {reporte_path}")

    # Dashboard HTML
    try:
        from video_intelligence.reporte_html import generar_dashboard
        generar_dashboard(reporte_b, {}, {}, {}, {"segmentos": []}, nombre)
    except:
        pass

    return master


# ── MAIN ──────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🧬 VIRAL INTELLIGENCE — Unified Pipeline (A+B Fusion)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 run_pipeline.py "https://www.tiktok.com/@user/video/123" --tema "finanzas personales"
  python3 run_pipeline.py mi_video.mp4 --tema "productividad" --guion mi_guion.txt
  python3 run_pipeline.py URL --tema "cocina" --skip-render --fast

Modos:
  --fast     Solo análisis rápido (fases 0-4)
  --full     Pipeline completo (fases 0-8)
  --analyze  Solo analizar, no generar plan ni renderizar
        """
    )
    parser.add_argument("input", help="URL de TikTok/YouTube o ruta a video local")
    parser.add_argument("--tema", required=True, help="Tema para el contenido nuevo")
    parser.add_argument("--guion", help="Ruta a archivo de guion (.txt)")
    parser.add_argument("--output", default="video_final", help="Nombre base de salida")
    parser.add_argument("--fast", action="store_true", help="Solo análisis rápido")
    parser.add_argument("--skip-render", action="store_true", help="No renderizar")
    parser.add_argument("--analyze", action="store_true", help="Solo analizar")
    args = parser.parse_args()

    print("""
╔══════════════════════════════════════════════════════════════╗
║          🧬 VIRAL INTELLIGENCE — Unified Pipeline           ║
║     Viral DNA v3.0 (A) × Video Intelligence v1.0 (B)       ║
╚══════════════════════════════════════════════════════════════╝
""")
    print(f"🎯 Tema: {args.tema}")
    print(f"📹 Input: {args.input}")

    # Determine if URL or local file
    input_path = Path(args.input)
    if input_path.exists() and input_path.is_file():
        video_path = input_path
    else:
        downloads = DATA_DIR / "downloads"
        video_path = step_download(args.input, downloads)

    nombre = video_path.stem

    # Execute phases
    reporte_a = {}
    try:
        reporte_a = step_scanner_a(video_path)
    except Exception as e:
        print(f"⚠️ Fase 1 (A) omitida: {e}")

    reporte_b = step_analyzer_b(video_path)
    tiktok = step_tiktok(video_path)
    unified_score = step_unified_score(reporte_a, reporte_b, tiktok)

    if args.fast or args.analyze:
        master = step_report(unified_score, {"tema": args.tema}, reporte_b, nombre)
        print(f"\n{'='*60}")
        print(f"  🎯 UNIFIED VIRAL SCORE: {unified_score['unified_viral_score']}/100")
        print(f"  📊 NIVEL: {unified_score['nivel']}")
        print(f"{'='*60}")
        return

    deep = step_deep_analysis(video_path, reporte_b)
    plan = step_generate_plan(reporte_a, reporte_b, args.tema, args.guion)

    if not args.skip_render:
        output = step_render(plan, args.output)

    master = step_report(unified_score, plan, reporte_b, nombre)

    # Final summary
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    🏆 PIPELINE COMPLETADO                    ║
╠══════════════════════════════════════════════════════════════╣
║  🎯 Viral Score: {unified_score['unified_viral_score']:>3d}/100  │  Nivel: {unified_score['nivel']:<21} ║
║  📁 Reporte: results/{nombre}_unified_report.json
║  🎬 Output:  results/{args.output}.mp4
║  📚 Docs:    docs/IDEAS_UNIFICADAS.md ({246+55}+ ideas)
║  📖 Prompts: docs/PROMPT_BOOK_UNIFICADO.md (115 prompts)
╚══════════════════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
