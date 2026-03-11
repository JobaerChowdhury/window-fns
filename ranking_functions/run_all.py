"""
run_all.py — Run all ranking function tutorials and exercises in sequence.

Usage:
    # From the ranking_functions/ directory:
    python run_all.py

    # Or from the project root:
    python ranking_functions/run_all.py
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


# ── ROW_NUMBER() ─────────────────────────────────────────────────────────────
_banner("ROW_NUMBER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "row_number.py"))

_banner("ROW_NUMBER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "row_number.py"))

# ── RANK() ───────────────────────────────────────────────────────────────────
_banner("RANK() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "rank.py"))

_banner("RANK() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "rank.py"))

# ── DENSE_RANK() ─────────────────────────────────────────────────────────────
_banner("DENSE_RANK() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "dense_rank.py"))

_banner("DENSE_RANK() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "dense_rank.py"))

print(f"\n{_CYAN}{_BOLD}{'═' * 70}")
print("  🎉  All tutorials and exercises complete!")
print(f"{'═' * 70}{_RESET}\n")
