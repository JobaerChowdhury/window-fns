# SQL Window Functions — Ranking Functions Tutorial

A hands-on Python + DuckDB tutorial and exercise system covering the three
core SQL **ranking window functions**:

| Function | Ties same rank? | Gaps after tie? |
|---|---|---|
| `ROW_NUMBER()` | ❌ Always unique | — |
| `RANK()` | ✅ Yes | ✅ Yes |
| `DENSE_RANK()` | ✅ Yes | ❌ Never |

---

## Quick Start

```bash
# From the project root
source .venv/bin/activate

# ── Step 1: Learn (tutorials) ───────────────────────────────────
python ranking_functions/tutorials/row_number.py
python ranking_functions/tutorials/rank.py
python ranking_functions/tutorials/dense_rank.py

# ── Step 2: Practice (exercises) ───────────────────────────────
python ranking_functions/exercises/row_number.py
python ranking_functions/exercises/rank.py
python ranking_functions/exercises/dense_rank.py

# ── Or run everything at once ───────────────────────────────────
python ranking_functions/run_all.py
```

---

## Structure

```
ranking_functions/
├── setup.py            # Shared helpers (DB connection, printer, checker)
│
├── tutorials/          # Read & run — explains each function with examples
│   ├── row_number.py   # 3 × ROW_NUMBER() examples
│   ├── rank.py         # 3 × RANK() examples
│   └── dense_rank.py   # 3 × DENSE_RANK() examples
│
├── exercises/          # Practice — fill in SQL, run to check
│   ├── row_number.py   # 3 exercises for ROW_NUMBER()
│   ├── rank.py         # 3 exercises for RANK()
│   └── dense_rank.py   # 3 exercises for DENSE_RANK()
│
├── run_all.py          # Runs tutorials then exercises for all 3 functions
└── README.md           # This file
```

---

## How Tutorials Work

Each tutorial script runs automatically and prints:
1. A heading and explanation of the concept
2. The SQL demonstrating the concept
3. The result table from the retail dataset

Just run the file and read the output.

---

## How Exercises Work

Each exercise file has a `user_sql_N` variable with a placeholder:

```python
user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Quantity DESC)
"""
```

**To practice:**
1. Open e.g. `exercises/row_number.py`
2. Replace the `-- YOUR SQL HERE` comment with your SQL
3. Re-run: `python ranking_functions/exercises/row_number.py`
4. You'll see:
   - `✅ PASS — <what was validated>`
   - `❌ FAIL — <what went wrong>`  +  `💡 Hint: ...`

---

## Dataset

The exercises use the **Online Retail Dataset**
(`data/online-retail-dataset.csv`, ~540k rows).

| Column | Type | Description |
|---|---|---|
| `InvoiceNo` | VARCHAR | Transaction invoice number |
| `StockCode` | VARCHAR | Product code |
| `Description` | VARCHAR | Product name |
| `Quantity` | BIGINT | Units sold (negative = returns) |
| `InvoiceDate` | VARCHAR | Date/time of transaction |
| `UnitPrice` | DOUBLE | Price per unit |
| `CustomerID` | BIGINT | Customer identifier |
| `Country` | VARCHAR | Customer's country |
