#!/usr/bin/env python3
# Wrapper simple de loop_detector
import sys, subprocess
def main():
    if len(sys.argv) < 2: print("Uso: loop_validator.py video.mp4"); return
    subprocess.run(["python3", "video_intelligence/linea_tiempo.py", sys.argv[1]])
    print("Usá también loop_detector.py para análisis visual")
if __name__ == "__main__": main()
