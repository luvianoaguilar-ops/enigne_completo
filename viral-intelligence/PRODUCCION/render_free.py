#!/usr/bin/env python3
import sys, json, subprocess, shutil
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Uso: render_free.py plan.json output.mp4")
        sys.exit(1)

    plan = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out = Path(sys.argv[2])
    out.parent.mkdir(parents=True, exist_ok=True)

    tmp = out.parent / "_parts_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    parts = []
    for sc in plan.get("scenes", []):
        p = tmp / f"s_{sc['scene_id']:04d}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi",
            "-i", f"color=c=0x111111:s=1080x1920:r=30",
            "-t", str(sc["duration_sec"]),
            "-c:v", "libx264", "-preset", "fast",
            str(p)
        ], capture_output=True)
        parts.append(p)

    lst = tmp / "list.txt"
    lst.write_text("\n".join(f"file '{x.resolve()}'" for x in parts))

    silent = tmp / "silent.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(lst), "-c", "copy", str(silent)
    ], capture_output=True)

    shutil.copy2(silent, out)
    shutil.rmtree(tmp)
    print(f"✅ Renderizado: {out}")


if __name__ == "__main__":
    main()
