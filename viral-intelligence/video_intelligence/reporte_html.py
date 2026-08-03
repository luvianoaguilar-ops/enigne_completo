#!/usr/bin/env python3
"""Dashboard HTML interactivo con gráfico de energía y timeline."""
from __future__ import annotations
import json, html
from pathlib import Path
from .utils import RESULTS_DIR

def generar_dashboard(reporte, ocr, energia, camara, timeline, nombre_base):
    datos = {"reporte":reporte, "ocr":ocr, "energia":energia,
             "camara":camara, "timeline":timeline}
    datos_json = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    titulo = html.escape(f"Dashboard — {nombre_base}")
    # Self-contained HTML dashboard with embedded JS
    plantilla = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0"><title>__TITLE__</title>
<style>:root{--bg:#0b1020;--panel:#121a31;--text:#eaf0ff;--muted:#9ba8c7;--accent:#8b5cf6}
body{margin:0;font-family:system-ui;background:var(--bg);color:var(--text)}
main{width:min(1400px,94%);margin:32px auto}h1{margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:20px 0}
.card{background:var(--panel);border:1px solid #263252;border-radius:14px;padding:16px}
.label{color:var(--muted);font-size:12px;text-transform:uppercase}
.value{margin-top:8px;font-size:20px;font-weight:700}
.panel{background:var(--panel);border:1px solid #263252;border-radius:14px;padding:18px;margin-top:18px}
canvas{width:100%;height:260px;background:#0d1428;border-radius:10px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{padding:10px;text-align:left;border-bottom:1px solid #263252}
th{color:#c9d4f4}.tag{display:inline-block;background:#2a2355;color:#d8caff;
padding:4px 8px;border-radius:999px;margin:2px;font-size:12px}</style></head>
<body><main><h1>__TITLE__</h1><section class="grid" id="resumen"></section>
<section class="panel"><h2>Mapa de energía</h2><canvas id="grafico"></canvas></section>
<section class="panel"><h2>Timeline</h2><div style="overflow-x:auto">
<table><thead><tr><th>#</th><th>Tiempo</th><th>Fase</th><th>Energía</th>
<th>Texto</th><th>Cámara</th></tr></thead><tbody id="timeline"></tbody></table></div></section>
</main><script>const DATA=__DATA__;const e=v=>String(v??"").replaceAll("&","&amp;")
.replaceAll("<","&lt;").replaceAll(">","&gt;");const n=(v,d=2)=>{const x=Number(v??0);
return Number.isFinite(x)?x.toFixed(d):"0"};const r=DATA.reporte||{};const m=r.metadatos||{};
const v=m.video||{};const rec=r.receta||{};const hk=r.hook||{};const ed=r.visual?.edicion?.estadisticas_tomas||{};
const au=r.audio||{};const cards=[["Resolución",`${v.ancho||"?"}x${v.alto||"?"}`],
["FPS",n(v.fps)],["Duración",`${n(m.duracion_segundos,1)}s`],["Ritmo",ed.ritmo||"N/D"],
["BPM",n(au.bpm_estimado)],["Hook",hk.nota||"N/D"],["Cortes",r.visual?.edicion?.total_cortes??0],
["Sincronía",`${n((r.sincronia?.porcentaje||0)*100,0)}%`]];
document.getElementById("resumen").innerHTML=cards.map(([l,v])=>
`<div class="card"><div class="label">${e(l)}</div><div class="value">${e(v)}</div></div>`).join("");
const segs=DATA.timeline?.segmentos||[];
document.getElementById("timeline").innerHTML=segs.map(s=>
`<tr><td>${s.id}</td><td>${n(s.inicio)}→${n(s.fin)}</td>
<td><span class="tag">${e(s.fase)}</span></td><td>${n(s.energia_media)}</td>
<td>${e((s.texto||[]).join(" · "))}</td><td>${e((s.camara||[]).join(" · "))}</td></tr>`).join("");
function draw(){const c=document.getElementById("grafico"),ctx=c.getContext("2d"),
w=c.clientWidth*devicePixelRatio,h=c.clientHeight*devicePixelRatio;c.width=w;c.height=h;
ctx.scale(devicePixelRatio,devicePixelRatio);const cw=c.clientWidth,ch=c.clientHeight;
ctx.clearRect(0,0,cw,ch);const pts=DATA.energia?.puntos||[];
if(!pts.length){ctx.fillStyle="#9ba8c7";ctx.font="16px sans-serif";ctx.fillText("Sin datos",20,40);return}
ctx.strokeStyle="#263252";for(let i=0;i<=4;i++){const y=20+(ch-50)*(i/4);
ctx.beginPath();ctx.moveTo(40,y);ctx.lineTo(cw-15,y);ctx.stroke()}
const tMax=Math.max(...pts.map(p=>p.tiempo),1);ctx.beginPath();
pts.forEach((p,i)=>{const x=40+(p.tiempo/tMax)*(cw-55),y=ch-30-p.energia*(ch-55);
i===0?ctx.moveTo(x,y):ctx.lineTo(x,y)});ctx.strokeStyle="#8b5cf6";ctx.lineWidth=2.5;
ctx.stroke();ctx.fillStyle="#9ba8c7";ctx.font="12px sans-serif";
ctx.fillText("0s",40,ch-8);ctx.fillText(`${n(tMax,1)}s`,cw-60,ch-8)}
draw();window.addEventListener("resize",draw)</script></body></html>"""
    html_final = plantilla.replace("__TITLE__", titulo).replace("__DATA__", datos_json)
    salida = RESULTS_DIR / f"{nombre_base}_dashboard.html"
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html_final)
    print(f"✅ Dashboard: {salida}")
    return salida
