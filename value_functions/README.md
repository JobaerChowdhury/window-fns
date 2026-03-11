# Value Functions — Tutorial & Exercise Guide

A self-paced learning module for SQL **value window functions** using the
Online Retail Dataset (~540k rows) and DuckDB.

## Functions Covered

| Function | What it does |
|---|---|
| `LAG()` | Returns a value from a previous row in the partition |
| `LEAD()` | Returns a value from a future row in the partition |
| `FIRST_VALUE()` | Returns the first value in the window frame |
| `LAST_VALUE()` | Returns the last value in the window frame |

## Directory Structure

```
value_functions/
├── setup.py            # Shared helpers: DuckDB connection, pretty-printer, ✅/❌ checker
│
├── tutorials/          # Explanation + worked examples (read & run)
│   ├── lag.py          # 3 tutorials for LAG()
│   ├── lead.py         # 3 tutorials for LEAD()
│   ├── first_value.py  # 3 tutorials for FIRST_VALUE()
│   └── last_value.py   # 3 tutorials for LAST_VALUE()
│
├── exercises/          # Practice problems (fill in SQL, auto-checked)
│   ├── lag.py          # 3 exercises for LAG()
│   ├── lead.py         # 3 exercises for LEAD()
│   ├── first_value.py  # 3 exercises for FIRST_VALUE()
│   └── last_value.py   # 3 exercises for LAST_VALUE()
│
├── run_all.py          # Runs all tutorials followed by all exercises
└── README.md           # This file
```

## How to Use

```bash
# Activate the virtual environment (from project root)
source .venv/bin/activate

# Step 1: Read & run a tutorial to learn the function
python value_functions/tutorials/lag.py
python value_functions/tutorials/lead.py
python value_functions/tutorials/first_value.py
python value_functions/tutorials/last_value.py

# Step 2: Solve the exercises
python value_functions/exercises/lag.py
python value_functions/exercises/lead.py
python value_functions/exercises/first_value.py
python value_functions/exercises/last_value.py

# Or run everything at once
python value_functions/run_all.py
```

## Exercise Workflow

1. Open an exercise file (e.g. `exercises/lag.py`)
2. Find a `user_sql_N` variable with a `-- YOUR SQL HERE` comment
3. Replace the comment with your SQL
4. Run the file — it prints `✅ PASS` or `❌ FAIL` with a hint
5. Fix and re-run as needed

## Key Gotchas

- **`LAST_VALUE()` frame clause** — The default frame only looks back to
  the current row, so `LAST_VALUE()` returns the current row's own value.
  Always add `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`
  to get the true last value in the partition.

- **`FIRST_VALUE()` with full frame** — Same recommendation for
  consistency and to avoid surprises.

- **`LAG` / `LEAD` defaults** — Pass a third argument to avoid NULLs on
  boundary rows, e.g. `LAG(revenue, 1, 0)`.
