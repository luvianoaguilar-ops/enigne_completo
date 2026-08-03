#!/usr/bin/env python3
import sys, subprocess


def preguntar(prompt, modelo="llama3.2:3b"):
    try:
        r = subprocess.run(
            ["ollama", "run", modelo, prompt],
            capture_output=True, text=True, timeout=120
        )
        return r.stdout.strip()
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: ai_local.py 'prompt'")
        sys.exit(1)
    print(preguntar(" ".join(sys.argv[1:])))
