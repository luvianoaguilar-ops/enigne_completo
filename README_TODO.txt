═══════════════════════════════════════════════════════
  README — TODO LO DE ESTE CHAT
  3 de agosto 2026
═══════════════════════════════════════════════════════

Tenés razón: me estaba trabando y repitiendo.
Acá está todo ordenado.


╔═══════════════════════════════════════════════════╗
║  1. TUS ARCHIVOS (los 4 que usás)                 ║
╚═══════════════════════════════════════════════════╝

  ABRIR_ESTO.html        7 KB    el menú: "¿qué querés hacer?"
  MAPA_REAL_V120.html    663 KB  hace el video de geografía
  CHAT.html              124 KB  25 tops + 17 curiosidades + medir videos
  32_VIDEOS_LISTOS.txt   21 KB   los guiones escritos

  Están en /Users/mac/Desktop/MULTICUENTAS_ENGINE/

  Aparte tenés (de antes):
  ENGINE.html            el de muchas apps, cualquier nicho
  IMAGE_BRIDGE_V3.html   las imágenes


╔═══════════════════════════════════════════════════╗
║  2. QUÉ HICIMOS EN ESTE CHAT                      ║
╚═══════════════════════════════════════════════════╝

── LA KEY DE GOOGLE ──
Tu key empezaba con AQ. y el chat la rechazaba.
Google cambió el formato en junio 2026 y además esas
keys no andan con ?key= en la URL: van por header.
ARREGLADO. Después Google apagó los modelos viejos
(gemini-2.0) y también lo arreglé: ahora el chat
le PREGUNTA a Google qué modelos existen.

── MEDIR 42 VIDEOS DE 7 CANALES ──
Bajé y medí yo: chris_torr9, yellow.geo, mundo_xplora,
mundo.mapas, talesdelglobo, maplogue, geopianet.

LAS 6 REGLAS DEL GÉNERO (iguales en los 7):
   duración      72,1s
   brillo        35,2%
   saturación    58,4%
   contraste     40,5
   verde         13,0%
   cámara cv      0,90   ← LA LEY

De 42 videos, CERO tienen cámara pareja. Todos tiemblan.
Si la tuya se mueve parejito, se nota que es código.

LO QUE NO ES REGLA (cada canal hace lo suyo):
   temperatura (va de -14,8 a +27,9)
   viñeta · cortes/min · subtítulos

⚠️ El "enfriar el cuadro" que te hice lo SAQUÉ:
perseguía el -19 del Atacama, que era de ESE video.

Y corregí la ficha vieja: el contraste decía 89,
es 40,5. Le errábamos por más del doble.

── CONTENIDO: 25 TOPS + 17 CURIOSIDADES ──
Datos del Banco Mundial y Wikipedia, con fuente y año.
Ninguno lo inventó una IA.
Los segundos ya vienen con el ritmo medido.

Bug que arreglé: los tops traían países que el mapa
NO puede pintar (Mónaco, Palaos, Singapur) y el bloque
salía negro. Crucé 217 países del Banco Mundial contra
172 del mapa por código ISO. Ahora solo usa los que existen.

── LAS 4 CAPAS DEL VIDEO (lo que pediste viendo canales) ──

   0,00s  el mapa lejos, quieto
   0,12s  CAE hacia el país (ves 3x más territorio)
   0,90s  la línea blanca se dibuja sola, como birome
   1,55s  la bandera BARRE el país de izq a der
   2,30s  aparece el cartel con el nombre
   2,50s  el contorno cerró

Nada aparece de golpe. Todo entra en orden.

Todo medido con pipeta de las fotos que mandaste:
   borde       RGB(240,240,237), núcleo 4px, halo 1px
   cartel      fondo RGB(11,26,56) azul oscuro, NO negro
   amarillo    el tuyo RGB(214,188,58), la foto RGB(216,197,82)
               → el color ya estaba bien, faltaba el BRILLO

── LOS 3 BUGS DE LA ÚLTIMA RADIOGRAFÍA (V120) ──

1. La línea aparecía en 6 de 48 frames.
   Causa: la cámara mueve y gira el mapa, pero yo
   dibujaba la línea en coordenadas fijas. Quedaba
   en otro lado.
   → Ahora guardo la transformación de la cámara.

2. El neón medía 173→166→163: plano.
   Causa: pintaba el glow ANTES del país y el amarillo
   lo tapaba.
   → Ahora va después y sale hacia afuera.

3. La caída arrancaba con 32,8% de amarillo.
   Causa: el freno de cámara multiplica el zoom por
   0,30, así que mi 0,42 quedaba en 0,83.
   → Ahora arranca en 0,34 sin pasar por el freno.

── TU PROYECTO DE GITHUB ──
viral_inteligencia: 79 módulos Python.
Miré todo. Torch y Whisper NO los usa ninguno
(el requirements los pide al pedo, son 4 GB).

9 módulos andan con solo opencv+numpy:
   tiktok_hook_analyzer      score de los primeros 3s
   movimiento_camara         zoom/paneo/a mano/estática
   detector_subtitulos       legibilidad y zona segura
   salient_maps              dónde mira el ojo
   linea_tiempo · detector_duplicados
   control_continuidad · auto_crop_vertical
   tiktok_retention_curve


╔═══════════════════════════════════════════════════╗
║  3. QUÉ TENÉS INSTALADO (confirmado hoy)          ║
╚═══════════════════════════════════════════════════╝

   ✅ cv2 5.0.0
   ✅ scenedetect
   ❌ librosa          ← falta
   ✅ ollama: llama3.2:3b · qwen2.5:3b · llama3.2:1b

   librosa es para los 5 módulos de AUDIO.
   Si lo querés: pip3 install librosa soundfile


╔═══════════════════════════════════════════════════╗
║  4. LO QUE QUEDÓ A MEDIAS                         ║
╚═══════════════════════════════════════════════════╝

  A) EL VIDEO DEL TOP 10
     Tenés el V120 bajado. Falta cargar el guion,
     poner los países y grabar.
     Nunca terminamos uno con las 4 capas andando.

  B) CONECTAR TU PROYECTO DE GITHUB
     Te iba a armar UN comando que corre los 9 módulos
     sobre un video y escupe un .json para arrastrar
     al chat. No llegué a hacerlo.

  C) EL ENGINE
     El Topic PRO tiene el guion de Malvinas QUEMADO
     adentro. Si escribís "Sahara" te da el mismo
     guion con otro título. Sin arreglar.

  D) NO TENÉS NINGÚN VIDEO SUBIDO TODAVÍA
     Eso es lo que importa. Necesitás monetizar.


╔═══════════════════════════════════════════════════╗
║  5. MI RECOMENDACIÓN PARA MAÑANA                  ║
╚═══════════════════════════════════════════════════╝

  Hacer UNA sola cosa: EL VIDEO.

  1. Abrí MAPA_REAL_V120.html
  2. 📥 PEGAR EL GUION (cuadro grande de abajo)
  3. Poné los 12 países
  4. 🎵 ELEGIR PISTA
  5. 🗺️ GENERAR
  6. 🎬 CREAR VIDEO
  7. Subilo a TikTok

  Lo de GitHub y el ENGINE quedan para después.
  Llevás días sin subir nada y eso es lo único
  que te va a dar plata.


╔═══════════════════════════════════════════════════╗
║  6. EL GUION LISTO PARA PEGAR                     ║
╚═══════════════════════════════════════════════════╝

1|10.5|Este país suma una ciudad entera de gente todos los años.
2|4|Número 10: Rep. Dem. del Congo. 3,2 % por año.
3|4|Número 9: Níger. 3,2 % por año.
4|4.5|Número 8: Somalia. 3,3 % por año.
5|4.5|Número 7: Rep. Centroafricana. 3,4 % por año.
6|5|Número 6: Chad. 3,4 % por año.
7|5.5|Número 5: Siria. 3,8 % por año.
8|6|Número 4: Catar. 3,9 % por año.
9|6.5|Número 3: Omán. 4,0 % por año.
10|7.5|Número 2: Arabia Saudita. 4,6 % por año.
11|9|Número 1: Emiratos Árabes. 4,7 % por año.
12|5|¿Cuál te sorprendió más? Contame abajo.

LOS PAÍSES (en inglés, tal cual):
   1  United Arab Emirates
   2  Dem. Rep. Congo
   3  Niger
   4  Somalia
   5  Central African Rep.
   6  Chad
   7  Syria
   8  Qatar
   9  Oman
   10 Saudi Arabia
   11 United Arab Emirates
   12 United Arab Emirates

LOS CONTROLES:
   🟡 Amarillo neón          → Neón
   🏷️ Cartel                 → Como el canal
   ✨ Brillo del borde        → Como el canal
   ✏️ Contorno se dibuja solo → Sí
   🏳️ Bandera                → Sí, barre
   🧊 Enfriar                → Apagado


═══════════════════════════════════════════════════════
  ESTADO: 32 tests · 1473 verdes · 0 rojas
  El mapa NO se tocó nunca.
═══════════════════════════════════════════════════════
