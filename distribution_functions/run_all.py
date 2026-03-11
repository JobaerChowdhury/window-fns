"""
run_all.py — Run all distribution function tutorials and exercises in sequence.

Usage:
    # From the distribution_functions/ directory:
    python run_all.py

    # Or from the project root:
    python distribution_functions/run_all.py
"""

import os, runpy

_CYAN  = "\033[96m"
_BOLD  = "\033[1m"
_RESET = "\033[0m"

HERE = os.path.dirname(os.path.abspath(__file__))


def _banner(text: str) -> None:
    width = 70
    print(f"\n\n{_CYAN}{'█' * width}")
    print(f"  {_BOLD}{text}{_RESET}{_CYAN}")
    print(f"{'█' * width}{_RESET}\n")


# ── NTILE() ────────────────────────────────────────────────────────────────
_banner("NTILE() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "ntile.py"))

_banner("NTILE() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "ntile.py"))

# ── CUME_DIST() ────────────────────────────────────────────────────────────
_banner("CUME_DIST() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "cume_dist.py"))

_banner("CUME_DIST() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "cume_dist.py"))

# ── PERCENT_RANK() ─────────────────────────────────────────────────────────
_banner("PERCENT_RANK() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "percent_rank.py"))

_banner("PERCENT_RANK() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "percent_rank.py"))

print(f"\n{_CYAN}{_BOLD}{'═' * 70}")
print("  🎉  All distribution function tutorials and exercises complete!")
print(f"{'═' * 70}{_RESET}\n")
