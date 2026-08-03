#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime
def main():
    adn = json.loads(Path(sys.argv[1]).read_text())
    guion = Path(sys.argv[2]).read_text()
    tema = sys.argv[3]
    words = re.findall(r"\w+", guion)
    plan = {"topic": tema, "created": datetime.now().isoformat(), "scenes": []}
    idx = 0
    for esc in adn["escenas"]:
        dur = esc["duracion_seg"]
        cap = int(dur * 2.7)
        txt = " ".join(words[idx:idx + cap])
        idx += cap
        plan["scenes"].append({"id": esc["escena"], "dur": dur, "voice": txt, "visual": f"B-roll original sobre {tema}"})
    Path("visual_plan.json").write_text(json.dumps(plan, indent=2, ensure_ascii=False))
    print("✅ visual_plan.json")
if __name__ == "__main__": main()
