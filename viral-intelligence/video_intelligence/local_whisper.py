#!/usr/bin/env python3
import sys, subprocess, json
from pathlib import Path
def main():
    subprocess.run(["python3", "UTILS/transcribe_free.py", sys.argv[1], "base"])
if __name__ == "__main__": main()
