"""
setup.py — Shared helpers for the Distribution Functions tutorial.

Provides:
  - get_connection() : creates an in-memory DuckDB connection and loads the
                       retail_data view from the local CSV.
  - run_tutorial()   : pretty-prints a tutorial step (heading + SQL result).
  - check_exercise() : runs the user's SQL and validates it with an assertion
                       function, printing ✅ PASS or ❌ FAIL.
"""

import os
import textwrap

import duckdb
import pandas as pd

# ── Path helpers ────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
_CSV  = os.path.join(_HERE, "..", "data", "online-retail-dataset.csv")


def get_connection() -> duckdb.DuckDBPyConnection:
    """Return an in-memory DuckDB connection with the retail_data view loaded."""
    con = duckdb.connect(database=":memory:")
    con.execute(
        f"CREATE VIEW retail_data AS "
        f"SELECT * FROM read_csv_auto('{_CSV}')"
    )
    return con


# ── Display helpers ──────────────────────────────────────────────────────────
_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_CYAN   = "\033[96m"
_GREEN  = "\033[92m"
_RED    = "\033[91m"
_YELLOW = "\033[93m"
_DIM    = "\033[2m"


def _section(title: str) -> None:
    width = 70
    print(f"\n{_CYAN}{_BOLD}{'─' * width}{_RESET}")
    print(f"{_CYAN}{_BOLD}  {title}{_RESET}")
    print(f"{_CYAN}{_BOLD}{'─' * width}{_RESET}\n")


def _code_block(sql: str) -> None:
    """Print SQL in a dimmed code block."""
    dedented = textwrap.dedent(sql).strip()
    for line in dedented.splitlines():
        print(f"  {_DIM}{line}{_RESET}")
    print()


def _print_df(df: pd.DataFrame, max_rows: int = 15) -> None:
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 120)
    pd.set_option("display.max_colwidth", 40)
    print(df.head(max_rows).to_string(index=False))
    if len(df) > max_rows:
        print(f"  ... ({len(df)} rows total, showing first {max_rows})")
    print()


# ── Public API ───────────────────────────────────────────────────────────────

def run_tutorial(
    title: str,
    description: str,
    sql: str,
    con: duckdb.DuckDBPyConnection,
    max_rows: int = 15,
) -> pd.DataFrame:
    """
    Display a tutorial step: heading, explanation, SQL, and result table.

    Returns the result DataFrame so callers can inspect it if needed.
    """
    _section(f"📚 Tutorial: {title}")
    # Description (word-wrapped)
    for line in textwrap.wrap(description, width=68):
        print(f"  {line}")
    print()
    print(f"  {_BOLD}SQL:{_RESET}")
    _code_block(sql)
    print(f"  {_BOLD}Result:{_RESET}")
    df = con.execute(sql).df()
    _print_df(df, max_rows=max_rows)
    return df


def check_exercise(
    number: int,
    description: str,
    user_sql: str,
    validation_fn,
    con: duckdb.DuckDBPyConnection,
    hint: str = "",
) -> bool:
    """
    Run user_sql and validate the result with validation_fn(df) -> (bool, str).

    validation_fn should return a tuple: (passed: bool, message: str).
    Prints ✅ PASS or ❌ FAIL with a hint.
    Returns True on pass, False on fail.
    """
    label = f"Exercise {number}: {description}"
    _section(f"✏️  {label}")

    # Strip SQL-style line comments (-- ...) and check if anything real remains
    import re as _re
    _stripped = _re.sub(r"--[^\n]*", "", user_sql or "").strip()
    if not _stripped:
        print(f"  {_RED}❌ FAIL — No SQL provided. Fill in the 'user_sql' variable.{_RESET}\n")
        if hint:
            print(f"  {_YELLOW}💡 Hint: {hint}{_RESET}\n")
        return False

    print(f"  {_BOLD}Your SQL:{_RESET}")
    _code_block(user_sql)

    try:
        df = con.execute(user_sql).df()
    except Exception as exc:
        print(f"  {_RED}❌ FAIL — SQL error: {exc}{_RESET}\n")
        if hint:
            print(f"  {_YELLOW}💡 Hint: {hint}{_RESET}\n")
        return False

    print(f"  {_BOLD}Your result (first 10 rows):{_RESET}")
    _print_df(df, max_rows=10)

    try:
        passed, message = validation_fn(df)
    except Exception as exc:
        passed, message = False, f"Validation error: {exc}"

    if passed:
        print(f"  {_GREEN}✅ PASS — {message}{_RESET}\n")
    else:
        print(f"  {_RED}❌ FAIL — {message}{_RESET}\n")
        if hint:
            print(f"  {_YELLOW}💡 Hint: {hint}{_RESET}\n")

    return passed


def print_header(module_title: str, intro: str) -> None:
    """Print the top-of-module heading and intro text."""
    width = 70
    print(f"\n{'═' * width}")
    print(f"  🪟  {_BOLD}{module_title}{_RESET}")
    print(f"{'═' * width}")
    for line in textwrap.wrap(intro, width=68):
        print(f"  {line}")
    print()
