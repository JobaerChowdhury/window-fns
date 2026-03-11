# Aggregate Functions — Tutorial + Exercise Module

A self-paced practice module for **SQL aggregate window functions** using the Online Retail dataset and DuckDB.

## Structure

```
aggregate_functions/
├── setup.py              # Shared helpers: DuckDB connection, printer, ✅/❌ checker
│
├── tutorials/            # Explanation + worked examples (read & run)
│   ├── sum.py            # 3 tutorials for SUM() OVER()
│   ├── avg.py            # 3 tutorials for AVG() OVER()
│   ├── count.py          # 3 tutorials for COUNT() OVER()
│   ├── min.py            # 3 tutorials for MIN() OVER()
│   └── max.py            # 3 tutorials for MAX() OVER()
│
├── exercises/            # Practice problems (fill in SQL, auto-checked)
│   ├── sum.py            # 3 exercises for SUM() OVER()
│   ├── avg.py            # 3 exercises for AVG() OVER()
│   ├── count.py          # 3 exercises for COUNT() OVER()
│   ├── min.py            # 3 exercises for MIN() OVER()
│   └── max.py            # 3 exercises for MAX() OVER()
│
└── run_all.py            # Runs all tutorials followed by all exercises
```

## How to use

### Step 1 — Read and run the tutorial

```bash
# From the project root (activate venv first)
python aggregate_functions/tutorials/sum.py
```

Each tutorial file explains the function, shows three worked examples, and prints results against the real dataset.

### Step 2 — Fill in and run the exercises

Open the corresponding exercise file, replace the `-- YOUR SQL HERE` placeholder with your own SQL, then run:

```bash
python aggregate_functions/exercises/sum.py
```

The checker prints `✅ PASS` or `❌ FAIL` with a hint. Iterate until all three exercises pass.

### Step 3 — Run everything at once

```bash
python aggregate_functions/run_all.py
```

## Functions covered

| Function | Tutorial Topics | Exercise Topics |
|---|---|---|
| `SUM() OVER()` | Country total vs grand total; running cumulative spend; rolling 3-invoice total | Country + grand total; cumulative revenue per customer; invoice as % of customer total |
| `AVG() OVER()` | Country price benchmark; running avg invoice value; 3-invoice moving average | Country + global avg price; running avg with above/below flag; 3-invoice moving avg |
| `COUNT() OVER()` | Total invoices per customer; running row counter; NULL-aware % identified | Country + global row count; running row seq per customer; % identified customers |
| `MIN() OVER()` | Cheapest price per country; running min spend; earliest purchase date | Country + global min price; running min revenue; first purchase date + days elapsed |
| `MAX() OVER()` | Priciest product per country; personal-best invoice tracker; peak quantity | Country + global max price; running max + new-record flag; latest purchase + days remaining |
