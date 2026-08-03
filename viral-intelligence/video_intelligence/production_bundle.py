#!/usr/bin/env python3
import sys, json
from pathlib import Path
def main():
    d = json.loads(Path(sys.argv[1]).read_text())
    md = [f"# Bundle {d['project']['topic']}", f"Duración: {sum(s['duration_sec'] for s in d['scenes'])}s"]
    for s in d["scenes"]:
        md.append(f"## Escena {s['scene_id']} ({s['duration_sec']}s)\n- Voz: {s['voice_text']}\n- Visual: {s.get('original_visual',{}).get('type','')}")
    Path("bundle.md").write_text("\n".join(md))
    print("✅ bundle.md")
if __name__ == "__main__": main()
