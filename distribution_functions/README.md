# Distribution Functions — SQL Window Functions

This module covers the **distribution / statistical** SQL window functions:
`NTILE()`, `CUME_DIST()`, and `PERCENT_RANK()`.

## Structure

```
distribution_functions/
├── setup.py              # Shared helpers: DuckDB connection, pretty-printer, ✅/❌ checker
│
├── tutorials/            # Explanation + worked examples (read & run)
│   ├── ntile.py          # 3 tutorials for NTILE()
│   ├── cume_dist.py      # 3 tutorials for CUME_DIST()
│   └── percent_rank.py   # 3 tutorials for PERCENT_RANK()
│
├── exercises/            # Practice problems (fill in SQL, auto-checked)
│   ├── ntile.py          # 3 exercises for NTILE()
│   ├── cume_dist.py      # 3 exercises for CUME_DIST()
│   └── percent_rank.py   # 3 exercises for PERCENT_RANK()
│
├── solutions/            # Reference solutions (check here if stuck)
│   ├── ntile.py          # Solutions for NTILE() exercises
│   ├── cume_dist.py      # Solutions for CUME_DIST() exercises
│   └── percent_rank.py   # Solutions for PERCENT_RANK() exercises
│
├── run_all.py            # Runs all tutorials followed by all exercises
└── README.md             # This file
```

## Quick Start

```bash
source ../.venv/bin/activate

# Tutorials (read & run first)
python tutorials/ntile.py
python tutorials/cume_dist.py
python tutorials/percent_rank.py

# Exercises (fill in SQL, then run)
python exercises/ntile.py
python exercises/cume_dist.py
python exercises/percent_rank.py

# Solutions (reference if stuck)
python solutions/ntile.py
python solutions/cume_dist.py
python solutions/percent_rank.py

# Or run everything at once
python run_all.py
```

## Function Summary

| Function | Returns | Range | First / Last |
|---|---|---|---|
| `NTILE(n)` | Integer bucket (1–n) | `[1, n]` | Bucket 1 = lowest rank |
| `CUME_DIST()` | Fraction of rows ≤ current | `(0, 1]` | Last row = 1.0 |
| `PERCENT_RANK()` | Rank-based fraction | `[0, 1]` | First row = 0.0, Last = 1.0 |

### Key Differences

- **NTILE** assigns discrete integer labels (quartiles, deciles) — great for segmentation.
- **CUME_DIST** counts what fraction of the partition is at or below the current value. Ties share the **highest** fractional value in the tie group.
- **PERCENT_RANK** uses `(RANK - 1) / (N - 1)`. Ties share the **lowest** fractional value in the tie group. Always starts at 0.0.
