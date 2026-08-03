#!/usr/bin/env python3
import sys, subprocess, re
def main():
    if len(sys.argv) < 2: print("Uso: silence_cutter.py video.mp4"); return
    cmd = ["ffmpeg", "-i", sys.argv[1], "-af", "silencedetect=noise=-30dB:d=0.3", "-f", "null", "-"]
    out = subprocess.run(cmd, capture_output=True, text=True).stderr
    starts = re.findall(r"silence_start:\s*([\d.]+)", out)
    print(f"Silencios: {len(starts)} - cortables con silence_killer.py")
if __name__ == "__main__": main()
