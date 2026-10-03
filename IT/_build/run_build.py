# -*- coding: utf-8 -*-
"""Build this module: markdown + xlsx + html + pdf."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
import generate  # noqa: E402

if __name__ == "__main__":
    sys.exit(generate.main(["generate", __import__("config").CONFIG.MODULE]))
