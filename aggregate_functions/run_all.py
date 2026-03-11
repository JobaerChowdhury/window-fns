"""
run_all.py — Run all aggregate function tutorials and exercises in sequence.

Usage:
    # From the aggregate_functions/ directory:
    python run_all.py

    # Or from the project root:
    python aggregate_functions/run_all.py
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


# ── SUM() OVER() ─────────────────────────────────────────────────────────────
_banner("SUM() OVER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "sum.py"))

_banner("SUM() OVER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "sum.py"))

# ── AVG() OVER() ─────────────────────────────────────────────────────────────
_banner("AVG() OVER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "avg.py"))

_banner("AVG() OVER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "avg.py"))

# ── COUNT() OVER() ───────────────────────────────────────────────────────────
_banner("COUNT() OVER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "count.py"))

_banner("COUNT() OVER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "count.py"))

# ── MIN() OVER() ─────────────────────────────────────────────────────────────
_banner("MIN() OVER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "min.py"))

_banner("MIN() OVER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "min.py"))

# ── MAX() OVER() ─────────────────────────────────────────────────────────────
_banner("MAX() OVER() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "max.py"))

_banner("MAX() OVER() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "max.py"))

print(f"\n{_CYAN}{_BOLD}{'═' * 70}")
print("  🎉  All aggregate function tutorials and exercises complete!")
print(f"{'═' * 70}{_RESET}\n")
