#!/usr/bin/env python3
import sys, json
from pathlib import Path
def main():
    if len(sys.argv) < 2: print("Uso: karaoke_subs.py transcribe_timing.json"); return
    segs = json.loads(Path(sys.argv[1]).read_text())
    ass = ["[Script Info]", "Title: Karaoke", "[V4+ Styles]",
           "Format: Name, Fontname, PrimaryColour, OutlineColour",
           "Style: Default,Arial Black,20,&H00FFFFFF,&H000000",
           "[Events]", "Format: Layer, Start, End, Style, Text"]
    def ts(s): return f"{int(s//3600)}:{int(s%3600//60):02d}:{int(s%60):02d}.{int(s%1*100):02d}"
    for i, s in enumerate(segs[:50]):
        ass.append(f"Dialogue: 0,{ts(s['inicio'])},{ts(s['fin'])},Default,{s['texto']}")
    Path("karaoke.ass").write_text("\n".join(ass))
    print("✅ karaoke.ass")
if __name__ == "__main__": main()
