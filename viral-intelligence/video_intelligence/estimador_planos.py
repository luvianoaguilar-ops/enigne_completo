#!/usr/bin/env python3
"""Estimador de tipos de plano con MediaPipe Pose + Face Detection."""
from __future__ import annotations
import argparse, json, cv2, numpy as np
from pathlib import Path
from .utils import RESULTS_DIR, guardar_json

def calc_prop(landmarks, w, h):
    if not landmarks: return 0.0
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
    except ImportError:
        return 0.0
    pts = [landmarks.landmark[p] for p in [
        mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_HIP, mp_pose.PoseLandmark.RIGHT_HIP,
        mp_pose.PoseLandmark.NOSE
    ] if landmarks.landmark[p].visibility > 0.5]
    if len(pts) < 3: return 0.0
    xs, ys = [p.x*w for p in pts], [p.y*h for p in pts]
    return ((max(xs)-min(xs))*(max(ys)-min(ys)))/(w*h)*100

def clasificar(pc, pr, tiene_cara):
    if tiene_cara:
        if pr>60: return "Primerísimo primer plano"
        if pr>40: return "Primer plano"
        if pr>20: return "Primer plano medio"
        if pc>50: return "Plano detalle"
        if pc>30: return "Plano medio corto"
        if pc>15: return "Plano medio"
        if pc>5: return "Plano americano"
        return "Plano entero"
    if pc>40: return "Plano detalle (objeto)"
    if pc>20: return "Plano medio (objeto)"
    if pc>5: return "Plano general medio"
    return "Gran plano general"

def estimar_planos(ruta, intervalo=0.5):
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        mp_face = mp.solutions.face_detection
    except ImportError:
        return {"error": "Instala: pip install mediapipe", "tomas": []}
    cap = cv2.VideoCapture(ruta)
    if not cap.isOpened(): raise RuntimeError("No se pudo abrir")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    salto = max(1, int(fps*intervalo))
    planos, fn, ultimo = [], 0, None
    with mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose, \
         mp_face.FaceDetection(static_image_mode=False, min_detection_confidence=0.5) as face:
        while True:
            ret, frame = cap.read()
            if not ret: break
            if fn%salto: fn+=1; continue
            t = fn/fps; h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pr = pose.process(rgb)
            pc = calc_prop(pr.pose_landmarks, w, h) if pr.pose_landmarks else 0.0
            fr = face.process(rgb)
            tiene, pr_val = False, 0.0
            if fr.detections:
                tiene = True
                for d in fr.detections:
                    b = d.location_data.relative_bounding_box
                    pr_val = max(pr_val, b.width*b.height*100)
            plano = clasificar(pc, pr_val, tiene)
            if plano != ultimo:
                planos.append({"frame":fn, "tiempo":round(t,3), "plano":plano,
                               "prop_cuerpo":round(pc,2), "prop_rostro":round(pr_val,2),
                               "tiene_cara":tiene})
                ultimo = plano
            fn+=1
    cap.release()
    res = {"video": Path(ruta).name, "intervalo": intervalo, "tomas": planos}
    salida = RESULTS_DIR / f"{Path(ruta).stem}_planos.json"
    guardar_json(str(salida), res)
    print(f"✅ Planos guardados: {salida}")
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--intervalo", type=float, default=0.5)
    args = parser.parse_args()
    estimar_planos(args.video, args.intervalo)
