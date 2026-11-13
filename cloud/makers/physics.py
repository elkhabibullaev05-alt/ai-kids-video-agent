#!/usr/bin/env python3
"""2026-11-13 owner: Money Story Daily (same Google account as Funny Rank) -> ranked funny physics Shorts.
Same engine as funny.py (CC BY clips only, credited), physics theme list."""
import os, runpy, sys
os.environ["FR_THEMES"] = "physics"
os.environ["FR_BRAND"] = "Physics Rank Daily"
os.environ["FR_TAGS"] = "#shorts #physics #science #fails #ranking"
sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "funny.py")
runpy.run_path(sys.argv[0], run_name="__main__")
