#!/usr/bin/env python3
import sys, json, cv2, numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
def main():
    frames = list(Path(sys.argv[1]).glob("*.jpg"))[:10]
    pixels = []
    for f in frames:
        img = cv2.imread(str(f))
        pixels.append(cv2.cvtColor(cv2.resize(img, (50, 50)), cv2.COLOR_BGR2RGB).reshape(-1, 3))
    data = np.vstack(pixels)
    km = KMeans(n_clusters=5, n_init=10).fit(data)
    pal = [{"hex": "#%02X%02X%02X" % tuple(c.astype(int))} for c in km.cluster_centers_]
    Path("palette.json").write_text(json.dumps(pal, indent=2))
    print(pal)
if __name__ == "__main__": main()
