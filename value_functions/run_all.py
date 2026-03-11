"""
run_all.py — Run all value function tutorials and exercises in sequence.

Usage:
    # From the value_functions/ directory:
    python run_all.py

    # Or from the project root:
    python value_functions/run_all.py
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


# ── LAG() ────────────────────────────────────────────────────────────────────
_banner("LAG() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "lag.py"))

_banner("LAG() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "lag.py"))

# ── LEAD() ───────────────────────────────────────────────────────────────────
_banner("LEAD() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "lead.py"))

_banner("LEAD() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "lead.py"))

# ── FIRST_VALUE() ────────────────────────────────────────────────────────────
_banner("FIRST_VALUE() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "first_value.py"))

_banner("FIRST_VALUE() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "first_value.py"))

# ── LAST_VALUE() ─────────────────────────────────────────────────────────────
_banner("LAST_VALUE() — Tutorials")
runpy.run_path(os.path.join(HERE, "tutorials", "last_value.py"))

_banner("LAST_VALUE() — Exercises")
runpy.run_path(os.path.join(HERE, "exercises", "last_value.py"))

print(f"\n{_CYAN}{_BOLD}{'═' * 70}")
print("  🎉  All value function tutorials and exercises complete!")
print(f"{'═' * 70}{_RESET}\n")
