# README DE RESCATE COMPLETO — MULTICUENTAS ENGINE — HASTA V37077

**Proyecto:** Multicuentas Engine / macOS-style local HTML app  
**Usuario:** Pablo  
**Estado actual:** V37077 — Low VRAM AI Generator Hub + Image Pack workflow en progreso  
**Fecha de rescate:** 2026-07-25  
**Objetivo de este README:** salvar todo lo hecho, explicar dónde estamos, qué logramos, qué falta y cómo seguir si el chat se traba.

---

# 1. Resumen ultra rápido

Llegamos a una etapa importante: el Engine ya no es solo un dashboard de ideas. Ahora tiene un flujo casi completo:

```txt
TikTok/YouTube referencia
↓
Video Watch Agent
↓
Frame PRO
↓
Pro Stack Director
↓
Topic PRO
↓
Asset PRO
↓
Export Pack
↓
AI Video Studio / Image Pack Importer
↓
Video local generado
```

Logramos crear videos reales en Mac usando Python, FFmpeg, MoviePy y Edge TTS. También logramos extraer frames de un TikTok real, aprender su estilo de mapa, aplicarlo al tema de Malvinas, generar guion y materiales, y crear un MP4 de prueba.

El último problema fue:

1. Pablo preguntó por qué las imágenes IA las tenía que generar el asistente y no el proyecto.
2. Se intentó pasar un ZIP con frames generados por IA, pero Arena marcó:

```txt
File not found in workspace
```

3. El chat empezó a trabarse y Pablo pidió este README de rescate.

---

# 2. Punto de partida anterior

Ya existían READMEs previos:

```txt
README_COMPLETO_FINAL_V37042_TODO (1).md
README_COMPLETO_CONTINUACION_V37053.md
README_FINAL_COMPLETO_TODO_LO_QUE_HICIMOS_MULTICUENTAS_V37053.md
```

Hasta V37053 ya se había documentado:

- V37042 SIMPLE IMPORTANT.
- V37043 GitHub Agents.
- V37044 Innovation Hub.
- V37045 Production Flow.
- V37046 Topic Intelligence.
- V37047 Asset Builder.
- V37048 Final Polish.
- V37049 Export Pack.
- V37050 AI Video Studio.
- V37053 Reference Agent Pro / Agente Deep.

Este README continúa desde ahí y rescata lo nuevo posterior.

---

# 3. Estado del Engine antes de la última etapa

El Engine actual estaba en:

```txt
~/Desktop/MULTICUENTAS_ENGINE/ENGINE.html
```

La versión fue avanzando hasta:

```txt
V37062 CLEAN UI
V37063 ADD TOPIC PRO
V37064 ASSET PRO STYLE AWARE
V37065 / V37066 Voice Lab PRO
V37067 Voice Director PRO
V37068 Map Visual PRO
V37070 MapLibre Director
V37071 MapLibre Recorder
V37072 Satellite Director
V37073 World Imagery Director
V37075 Visual Prompt Director PRO
V37076 Image Pack Importer
V37077 Low VRAM AI Generator Hub
```

---

# 4. Apps actuales importantes del Engine

Las apps principales útiles actualmente son:

```txt
👁️ Video Watch Agent
🖼️ Frame PRO
🧩 Pro Stack Director
🧠 Topic PRO
🎨 Asset PRO
📦 Export Pack
🎥 AI Video Studio
🎙️ Voice Lab PRO V2
🎬 Voice Director PRO
🗺️ Map Visual PRO / MapLibre tools
🎯 Visual Prompt PRO
🖼️ Image Pack Importer
🧠 Low VRAM AI Hub
🧹 App Cleaner
```

Las apps viejas se ocultaron con Clean UI / App Cleaner para no confundir:

```txt
Frame Analyzer viejo
Frame Analyzer FIX viejo
Topic Intel viejo
```

La app correcta para frames es:

```txt
🖼️ Frame PRO
```

La app correcta para guion con estilo aprendido es:

```txt
🧠 Topic PRO
```

La app correcta para materiales style-aware es:

```txt
🎨 Asset PRO
```

---

# 5. Logros principales

## 5.1. Se logró leer un TikTok real

Pablo usó un TikTok de referencia:

```txt
El desierto más árido del mundo. #atacama #chile
```

El agente consiguió:

```txt
source.mp4
source.info.json
analysis_summary.json
yt_dlp_log.txt
```

Luego se instaló FFmpeg y se pudieron extraer frames:

```txt
frame_01.jpg
frame_02.jpg
...
frame_08.jpg
```

Esto fue importante porque ya no dependíamos solo de describir el TikTok: el sistema pudo obtener frames reales.

---

## 5.2. Frame PRO aprendió el estilo visual

Se cargaron 8 frames en Frame PRO y el JSON correcto decía:

```json
"frames_count": 8
```

El estilo aprendido fue:

```txt
Mapa Satelital Educativo Viral
```

Características detectadas:

```txt
mapa satelital vertical 9:16
territorio resaltado amarillo/verde
borde brillante
zooms suaves
paneos
iconos explicativos
texto blanco grande con sombra negra
ritmo cada 3-6 segundos
voz clara, seria, documental corto
```

Se aplicó al tema:

```txt
historia de las islas malvinas en dibujo
```

Y produjo formato:

```txt
Malvinas Mapa Satelital Misterioso
```

---

## 5.3. Pro Stack Director entendió los frames

Primero Pro Stack ignoraba `frames_count`, pero se creó V37060 Frame Aware para que entendiera el JSON de Frame PRO.

Resultado correcto:

```json
"diagnostico": "✅ Se detectó perfil de frames cargados. El plan usa el estilo real del Frame PRO."
```

Esto conectó correctamente:

```txt
Frame PRO → Pro Stack Director
```

---

## 5.4. Topic PRO creó guion style-aware

Luego Topic PRO generó un guion ya adaptado al estilo aprendido:

```txt
V37063_TOPIC_PRO_STYLE_AWARE
```

Ejemplo de estructura:

```txt
0-3s: mapa satelital de Sudamérica, zoom al Atlántico Sur, Malvinas brillan en amarillo. Texto: MALVINAS.
3-8s: paneo desde Patagonia hacia las islas. Texto: ATLÁNTICO SUR.
8-15s: línea de tiempo sobre mapa. Texto: HISTORIA LARGA.
15-23s: pin rojo sobre islas, año 1833.
23-32s: 1982 con barcos simples, sin violencia.
32-43s: ONU + mapa actual + disputa.
43-55s: cierre con pregunta ¿QUÉ PASA HOY?
```

---

## 5.5. Asset PRO corrigió el Asset Builder viejo

Asset Builder viejo mezclaba overlays y sacaba cosas como:

```txt
Frame 2 con overlay LÍNEA DE TIEMPO cuando debía ser ATLÁNTICO SUR
Frame 4 con overlay 1982 cuando debía ser 1833
```

Por eso se creó:

```txt
V37064 ASSET PRO STYLE AWARE
```

Resultado correcto:

```txt
Frame 1: MALVINAS
Frame 2: ATLÁNTICO SUR
Frame 3: HISTORIA LARGA
Frame 4: 1833
Frame 5: 1982
Frame 6: DISPUTA
Frame 7: ¿QUÉ PASA HOY?
```

Y generó:

```txt
narracion_final
prompts_frame_por_frame
subtitulos_srt
descripcion
hashtags
plan_edicion
checklist
```

---

## 5.6. Export Pack generó `PACK_PRODUCCION.json`

Pablo tocó Export Pack y obtuvo:

```txt
PACK_PRODUCCION.json
```

Ese pack contiene toda la receta final:

- narración,
- prompts,
- overlays,
- captions,
- SRT,
- hashtags,
- plan de edición.

---

## 5.7. Se generó un primer MP4 local

Como el botón de AI Video Studio no descargaba bien, se creó:

```txt
CREAR_PROYECTO_VIDEO_DESDE_PACK_MAC.py
```

Ese script buscó el `PACK_PRODUCCION.json` y creó:

```txt
~/Desktop/VIDEO_MALVINAS_PRO
```

Con:

```txt
pack_produccion.json
render_video_malvinas_pro.py
RUN_VIDEO_MALVINAS_PRO.sh
README_VIDEO_MALVINAS_PRO.md
out/
```

Luego se generó:

```txt
video_malvinas_pro.mp4
voice.mp3
frame_01.png ... frame_07.png
narracion.txt
subtitulos.srt
prompts_dibujo.txt
descripcion_hashtags.txt
```

Esto fue un gran logro: ya había un video real, aunque visualmente básico.

---

# 6. Mejora de voz

## 6.1. Voice Lab PRO

Pablo dijo que la voz se notaba IA. Se generaron varias voces con Edge TTS:

```txt
voz_arg_tomas_masculina.mp3
voz_arg_elena_femenina.mp3
voz_mx_jorge_masculina.mp3
voz_mx_dalia_femenina.mp3
```

Pablo eligió:

```txt
voz_mx_jorge_masculina.mp3
```

como la mejor.

---

## 6.2. Voice Director PRO

Luego se detectó que el comienzo sonaba raro, como “estaas”. Se concluyó que no era solo la voz, sino el guion.

Se creó Voice Director PRO para:

- evitar comenzar con “Estas...”,
- usar frases más cortas,
- escribir años en palabras,
- agregar pausas,
- usar Jorge MX más lento.

Ejemplo:

```txt
Aunque parecen pequeñas,
las Malvinas marcaron la historia de dos países.

Mil ochocientos treinta y tres.
Mil novecientos ochenta y dos.
```

Se hicieron varios parches porque los primeros fallaron por comillas/caracteres internos en Python.

Estado: Voice Director PRO quedó encaminado pero se decidió seguir con visuales antes de verificar todo.

---

# 7. Mejora visual de mapas

## 7.1. Map Visual PRO

Primero se hizo:

```txt
MAP_VISUAL_PRO_MAC.py
```

Generaba mapas simulados con PIL:

```txt
mappro_frame_01.png...
video_malvinas_map_visual_pro.mp4
```

Pablo dijo que era mejor que lo anterior, pero todavía muy atrasado.

---

## 7.2. MapLibre Director

Se buscó GitHub y se usaron ideas de:

- Remotion MapLibre example,
- MapLibre GL video export,
- OpenMontage,
- MapLapse.

Se creó:

```txt
MAPLIBRE_DIRECTOR_MAC.py
```

Generó:

```txt
~/Desktop/MAPLIBRE_MALVINAS_PROJECT/index.html
```

Con mapa real en navegador, botones:

```txt
Reproducir
Siguiente
Reset
```

Esto se vio mejor.

---

## 7.3. MapLibre Recorder PRO

Se creó:

```txt
MAPLIBRE_RECORDER_PRO_MAC.py
```

Grabó el preview MapLibre con Playwright:

```txt
Frames grabados: 56
video_malvinas_maplibre_recorded_pro.mp4
```

Fue un avance: mapa real → frames automáticos → MP4 con voz.

---

## 7.4. Satellite Director PRO

Se buscó algo más satelital. Se usó inspiración de NASA Blue Marble / Geolonia:

```txt
MAPLIBRE_SATELLITE_DIRECTOR_MAC.py
```

Generó:

```txt
~/Desktop/MAPLIBRE_SATELLITE_MALVINAS_PROJECT/index.html
```

Se veía más satelital pero aún no suficientemente parecido al TikTok.

---

## 7.5. World Imagery Director PRO

Se creó:

```txt
MAPLIBRE_WORLD_IMAGERY_DIRECTOR_MAC.py
```

Con base tipo Esri World Imagery. Mejoró el detalle, pero el resaltado amarillo no estaba alineado perfecto.

---

## 7.6. World Imagery Align PRO

Se creó:

```txt
MAPLIBRE_WORLD_IMAGERY_ALIGN_PRO_MAC.py
```

Intentó alinear mejor el resaltado con:

- polígonos separados para East/West Falkland,
- controles de movimiento,
- slider de opacidad.

Aun así Pablo dijo que no se comparaba al TikTok.

---

# 8. Cambio de estrategia visual

Se concluyó:

```txt
MapLibre / OSM / Blue Marble / World Imagery mejoran, pero no llegan al look del TikTok.
```

El TikTok parece más:

```txt
Google Earth / imagen satelital cinematográfica / relieve fuerte / diseño editado
```

Entonces se decidió cambiar el enfoque:

```txt
No insistir solo con mapas web.
Usar frames como referencia estética.
Generar imágenes IA propias con prompts potentes.
```

---

# 9. Visual Prompt Director PRO

Se investigaron proyectos:

- CLIP Interrogator,
- ComfyUI IPAdapter,
- Krea2 StyleTransfer,
- Storyboard Prompt Generator,
- PromptMotion.

Se creó:

```txt
V37075 Visual Prompt Director PRO
```

Nueva app:

```txt
🎯 Visual Prompt PRO
```

Generó prompts por frame para imágenes estilo:

```txt
vertical 9:16 cinematic satellite geography short
Google Earth style flyover
realistic terrain relief
dark blue ocean
glowing yellow highlighted territory
bold white TikTok caption with black shadow
```

El JSON empieza con:

```json
"version": "V37075_VISUAL_PROMPT_DIRECTOR_PRO"
```

---

# 10. Low VRAM AI Hub

Pablo pidió integrar lo de proyectos estilo NVIDIA / low RAM / no sobrecargar.

Se investigaron:

- Wan2GP,
- LTX Video distilled / FP8,
- NVIDIA Model Optimizer,
- ComfyUI low VRAM,
- CLIP Interrogator low VRAM.

Se creó:

```txt
V37077 Low VRAM AI Generator Hub
```

Nueva app:

```txt
🧠 Low VRAM AI Hub
```

Explica stack:

```txt
Wan2GP: generator para GPU pobre, modelos Wan/LTX/Hunyuan/Flux/Qwen/TTS, cuantización.
LTX Video: distilled/fp8 para menos VRAM.
NVIDIA Model Optimizer: quantization/pruning/distillation.
ComfyUI IPAdapter: style reference.
CLIP Interrogator: image to prompt con low VRAM.
```

El JSON generado empieza:

```json
"version": "V37077_LOW_VRAM_AI_GENERATOR_HUB"
```

---

# 11. Problema actual: por qué las imágenes las generó el asistente y no el proyecto

Pablo preguntó:

> “¿Por qué tengo que pasarte el prompt a vos para generar las imágenes y no puedo hacerlo desde mi proyecto?”

Respuesta técnica:

El Engine actual es un HTML local. Puede:

- generar prompts,
- organizar imágenes,
- exportar packs,
- correr scripts locales,
- crear MP4 con Python.

Pero para generar imágenes IA directamente necesita uno de estos backends:

1. API externa:
   - Arena image generation,
   - Gemini image,
   - Leonardo,
   - OpenAI image,
   - etc.

2. Backend local:
   - ComfyUI,
   - Stable Diffusion,
   - Fooocus,
   - Draw Things,
   - Wan2GP,
   - LTX,
   - etc.

Actualmente no hay un backend de imágenes conectado al Engine. Por eso el asistente generó las imágenes desde su herramienta interna. El siguiente paso lógico es crear:

```txt
V37078 Image Generator Bridge
```

Para que el Engine pueda mandar prompts a un generador externo/local.

---

# 12. Problema del ZIP

Se generó un ZIP:

```txt
v37077_image_pack_malvinas.zip
```

pero Pablo dijo que al intentar descargarlo salió:

```txt
File not found in workspace
```

Esto puede pasar por:

- el archivo no persistió en el workspace,
- el chat se trabó,
- la herramienta `present_file` falló,
- Arena perdió referencia temporal.

Solución si pasa:

1. Regenerar ZIP.
2. O generar imágenes de nuevo.
3. O crear un script local para que el usuario use imágenes manuales en `IMAGE_PACK_MALVINAS`.

---

# 13. Image Pack Importer

Se creó:

```txt
IMAGE_PACK_IMPORTER_MAC.py
```

y parche:

```txt
PATCH_V37076_IMAGE_PACK_IMPORTER_AUTO_MAC.py
```

Nueva app:

```txt
🖼️ Image Pack Importer
```

Función:

```txt
imágenes buenas generadas por IA
↓
~/Desktop/IMAGE_PACK_MALVINAS
↓
Image Pack Importer
↓
ai_frame_01.png...
video_malvinas_image_pack_pro.mp4
```

El usuario debe poner imágenes en:

```txt
~/Desktop/IMAGE_PACK_MALVINAS
```

El script acepta:

```txt
.png
.jpg
.jpeg
.webp
```

---

# 14. Último avance: se generaron imágenes IA buenas

El asistente generó imágenes con `generate_image` a partir del JSON de Visual Prompt / Low VRAM Hub.

Se intentó pasar un ZIP, pero falló la descarga.

Las imágenes eran buenas y Pablo confirmó:

```txt
ese mapa fue bueno
este es mucho mejor socio
```

Por eso se decidió que hay que integrar **ese camino** al Engine.

---

# 15. Qué falta hacer inmediatamente

## 15.1. Crear V37078 Image Generator Bridge

Nueva app propuesta:

```txt
🧬 Image Generator Bridge
```

Funciones:

- Tomar JSON de Low VRAM AI Hub.
- Mostrar prompts frame por frame.
- Permitir copiar prompt individual.
- Permitir marcar imágenes generadas.
- Preparar carpeta `IMAGE_PACK_MALVINAS`.
- Opción futura de conectar APIs:
  - Arena/Gemini/Leonardo,
  - ComfyUI local,
  - Automatic1111,
  - Fooocus,
  - Draw Things,
  - Wan2GP.

Primera versión no necesita generar imágenes automáticamente; debe organizar el proceso y evitar confusión.

---

## 15.2. Crear V37079 ComfyUI / Wan2GP Setup Guide

Nueva app propuesta:

```txt
⚙️ AI Setup Guide
```

Debe explicar:

- si tenés Mac sin NVIDIA, usar externo/Arena/Gemini/Leonardo primero.
- si tenés NVIDIA, explorar Wan2GP / LTX / ComfyUI.
- si tenés poca VRAM, usar:
  - 768x1344,
  - attention slicing,
  - FP8/distilled,
  - low VRAM mode,
  - upscale posterior.

---

## 15.3. Regenerar frames si el ZIP falla

Si se necesita regenerar desde el asistente, usar prompts del JSON V37077 y crear:

```txt
frame_01.png
frame_02.png
frame_03.png
frame_04.png
frame_05.png
frame_06.png
frame_07.png
```

Luego crear ZIP o entregar individualmente.

---

# 16. Cómo continuar desde aquí

Si se abre un chat nuevo, pegar:

```txt
Continuamos el proyecto Multicuentas Engine. Estamos en V37077 Low VRAM AI Generator Hub. Ya logramos: Video Watch Agent extrajo frames de TikTok; Frame PRO aprendió estilo; Pro Stack Frame Aware lo entendió; Topic PRO generó guion style-aware; Asset PRO generó materiales; Export Pack generó PACK_PRODUCCION; Voice Lab/Director mejoró voz Jorge; MapLibre/World Imagery probaron mapas; finalmente Visual Prompt PRO + Low VRAM AI Hub generaron prompts muy buenos para imágenes IA. El problema actual: las imágenes IA buenas las generó el asistente, pero queremos integrarlo al Engine. Hay que crear V37078 Image Generator Bridge para que el proyecto maneje prompts/imágenes y prepare IMAGE_PACK_MALVINAS, y después V37079 para ComfyUI/Wan2GP/Low VRAM.
```

---

# 17. Estado actual exacto

## Engine actual aproximado

```txt
~/Desktop/MULTICUENTAS_ENGINE/ENGINE.html
```

Debe incluir hasta:

```txt
V37077 Low VRAM AI Hub
```

## Proyecto de video

```txt
~/Desktop/VIDEO_MALVINAS_PRO/out
```

Contiene varios videos:

```txt
video_malvinas_pro.mp4
video_malvinas_voicepro_jorge.mp4
video_malvinas_map_visual_pro.mp4
video_malvinas_maplibre_recorded_pro.mp4
video_malvinas_real_map_tiles_pro.mp4
```

Y audios:

```txt
voz_mx_jorge_masculina.mp3
voz_mx_jorge_director_v3.mp3
voice.mp3
```

## Carpeta para imágenes IA

```txt
~/Desktop/IMAGE_PACK_MALVINAS
```

Ahí deben ir las imágenes generadas por IA.

---

# 18. Logro principal del proyecto

El mayor logro hasta ahora:

```txt
Pasamos de una web estática con ideas a un Engine local que puede:
- leer referencias de TikTok/YouTube,
- extraer frames,
- aprender estilo,
- generar guion con contexto,
- generar materiales,
- crear voz,
- crear MP4,
- probar mapas reales,
- crear prompts IA para imágenes mejores.
```

El sistema todavía no es perfecto, pero ya tiene arquitectura real.

---

# 19. Próximo paso recomendado

Crear:

```txt
PATCH_V37078_IMAGE_GENERATOR_BRIDGE_AUTO_MAC.py
```

Nueva app:

```txt
🧬 Image Generator Bridge
```

Debe resolver exactamente la pregunta de Pablo:

> “¿Por qué tengo que pasarte a vos el prompt para generar imágenes? Quiero hacerlo desde el proyecto.”

Primera versión:

- no genera imágenes sola,
- pero organiza prompts,
- copia prompt por frame,
- prepara carpeta,
- permite importar resultados,
- manda a Image Pack Importer.

Segunda versión futura:

- conectar con API o ComfyUI.

---

# 20. Nota final

Este README se hizo porque el chat se trabó muchas veces. Sirve para rescatar el proyecto y continuar sin perder nada.

**Fin del README de rescate V37077.**
