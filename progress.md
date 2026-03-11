# Progress — SQL Window Functions Practice Project

## Project Overview

A self-paced, Python + DuckDB learning environment for SQL window functions.
The dataset used throughout is the **Online Retail Dataset** (`data/online-retail-dataset.csv`, ~540k rows).

**Stack:** Python · DuckDB (in-memory) · pandas

---

## Dataset Schema

| Column | Type | Description |
|---|---|---|
| `InvoiceNo` | VARCHAR | Transaction invoice number |
| `StockCode` | VARCHAR | Product code |
| `Description` | VARCHAR | Product name |
| `Quantity` | BIGINT | Units sold (negative = return) |
| `InvoiceDate` | VARCHAR | Date/time string (`M/D/YYYY H:MM`) |
| `UnitPrice` | DOUBLE | Price per unit |
| `CustomerID` | BIGINT | Customer identifier |
| `Country` | VARCHAR | Customer's country |

---

## Completed

### ✅ Phase 1 — Project Setup
- DuckDB in-memory connection wired up to local CSV (`data/online-retail-dataset.csv`)
- Explored dataset schema and sample queries (`first.py`)
- Prototype LAG() query (`lead.py`)
- Interview question lists compiled:
  - `interview-questions.md` — original list
  - `interview-questions-v2.md` — 20 advanced FAANG-level questions with concepts
  - `interview-solutions-v2.md` — solution file (questions + concepts, solutions separate)

### ✅ Phase 2 — Ranking Functions Tutorial (`ranking_functions/`)

A complete tutorial + exercise system for the three core ranking window functions,
with tutorials and exercises separated into their own directories.

```
ranking_functions/
├── setup.py            # Shared helpers: DuckDB connection, pretty-printer, ✅/❌ checker
├── validators.py       # Shared validation logic for exercises and solutions
│
├── tutorials/          # Explanation + worked examples (read & run)
│   ├── row_number.py   # 3 tutorials for ROW_NUMBER()
│   ├── rank.py         # 3 tutorials for RANK()
│   └── dense_rank.py   # 3 tutorials for DENSE_RANK()
│
├── exercises/          # Practice problems (fill in SQL, auto-checked)
│   ├── row_number.py   # 3 exercises for ROW_NUMBER()
│   ├── rank.py         # 3 exercises for RANK()
│   └── dense_rank.py   # 3 exercises for DENSE_RANK()
│
├── solutions/          # Reference solutions (check here if stuck)
│   ├── row_number.py   # Solutions for ROW_NUMBER() exercises
│   ├── rank.py         # Solutions for RANK() exercises
│   └── dense_rank.py   # Solutions for DENSE_RANK() exercises
│
├── run_all.py          # Runs all tutorials followed by all exercises
└── README.md           # User guide
```

#### Content per function (3 tutorials + 3 exercises each)

| Function | Tutorial Topics | Exercise Topics |
|---|---|---|
| `ROW_NUMBER()` | Global row numbering; per-customer purchase ordering; first-purchase extraction via CTE | Number lines by Quantity DESC per Country; find each customer's 2nd purchase; de-duplicate (InvoiceNo, StockCode) |
| `RANK()` | Global product ranking by qty (with gaps); per-country customer spend ranking; RANK vs ROW_NUMBER side-by-side | Rank countries by unique customers; rank StockCode by avg price per country; **top-15 France products: ROW_NUMBER, RANK, DENSE_RANK side-by-side — ties at rows 7–8 show RANK skipping a number while DENSE_RANK stays contiguous** |
| `DENSE_RANK()` | Dense rank by total revenue; per-country order-count ranking; all three functions side-by-side | Dense rank countries by sales (contiguous check); dense rank cheapest product per country; **top-15 Germany products by order count: ROW_NUMBER, RANK, DENSE_RANK side-by-side — multiple natural ties make RANK max > DENSE_RANK max visibly** |

#### How the exercise system works
- Each exercise file in `exercises/` has a `user_sql_N` placeholder
- Running the file prints `✅ PASS` or `❌ FAIL` with a descriptive message and hint
- To practice: replace the placeholder with your own SQL, re-run the file
- If stuck: check the matching file in `solutions/` — same validator, complete SQL included
- All 9 exercises verified: `python ranking_functions/run_all.py` → 9/9 ✅
- All 9 solutions verified: `python ranking_functions/solutions/*.py` → 9/9 ✅

---

### ✅ Phase 3 — Value Functions Tutorial (`value_functions/`)

A complete tutorial + exercise system for the four SQL value window functions,
following the same structure as the ranking_functions module.

```
value_functions/
├── setup.py              # Shared helpers: DuckDB connection, pretty-printer, ✅/❌ checker
├── validators.py         # Shared validation logic for exercises and solutions
│
├── tutorials/            # Explanation + worked examples (read & run)
│   ├── lag.py            # 3 tutorials for LAG()
│   ├── lead.py           # 3 tutorials for LEAD()
│   ├── first_value.py    # 3 tutorials for FIRST_VALUE()
│   └── last_value.py     # 3 tutorials for LAST_VALUE()
│
├── exercises/            # Practice problems (fill in SQL, auto-checked)
│   ├── lag.py            # 3 exercises for LAG()
│   ├── lead.py           # 3 exercises for LEAD()
│   ├── first_value.py    # 3 exercises for FIRST_VALUE()
│   └── last_value.py     # 3 exercises for LAST_VALUE()
│
├── solutions/            # Reference solutions (check here if stuck)
│   ├── lag.py            # Solutions for LAG() exercises
│   ├── lead.py           # Solutions for LEAD() exercises
│   ├── first_value.py    # Solutions for FIRST_VALUE() exercises
│   └── last_value.py     # Solutions for LAST_VALUE() exercises
│
├── run_all.py            # Runs all tutorials followed by all exercises
└── README.md             # User guide
```

#### Content per function (3 tutorials + 3 exercises each)

| Function | Tutorial Topics | Exercise Topics |
|---|---|---|
| `LAG()` | Previous invoice date per customer; revenue delta between consecutive invoices; consecutive same-country order detection | Previous Quantity per customer; revenue delta with 0 default; find invoices where country changed |
| `LEAD()` | Next invoice date per customer; days until next purchase; identify last purchase (LEAD IS NULL) | Next invoice number per customer; days until next purchase; find penultimate invoice |
| `FIRST_VALUE()` | First product ever bought per customer; cheapest price per country baseline; days since first purchase | First-ever StockCode on every row; cheapest avg price per country; days elapsed since first purchase |
| `LAST_VALUE()` | Most recent product on every row; priciest product per country; FIRST_VALUE vs LAST_VALUE side-by-side | Last-ever StockCode on every row; priciest avg price per country; customer lifetime days (FIRST + LAST combined) |

#### How the exercise system works
- Each exercise file in `exercises/` has a `user_sql_N` placeholder
- Running the file prints `✅ PASS` or `❌ FAIL` with a descriptive message and hint
- If stuck: check the matching file in `solutions/` — same validator, complete SQL included
- All 12 exercise SQL solutions verified before clearing: 12/12 ✅
- All 12 solutions verified: `python value_functions/solutions/*.py` → 12/12 ✅

---

### ✅ Phase 4 — Aggregate Functions Tutorial (`aggregate_functions/`)

A complete tutorial + exercise system for the five SQL aggregate window functions,
following the same structure as the ranking_functions and value_functions modules.

```
aggregate_functions/
├── setup.py              # Shared helpers: DuckDB connection, pretty-printer, ✅/❌ checker
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
├── solutions/            # Reference solutions (check here if stuck)
│   ├── sum.py            # Solutions for SUM() OVER() exercises
│   ├── avg.py            # Solutions for AVG() OVER() exercises
│   ├── count.py          # Solutions for COUNT() OVER() exercises
│   ├── min.py            # Solutions for MIN() OVER() exercises
│   └── max.py            # Solutions for MAX() OVER() exercises
│
├── run_all.py            # Runs all tutorials followed by all exercises
└── README.md             # User guide
```

#### Content per function (3 tutorials + 3 exercises each)

| Function | Tutorial Topics | Exercise Topics |
|---|---|---|
| `SUM() OVER()` | Country total vs grand total; running cumulative spend per customer; rolling 3-invoice total | Country + grand total on every row; cumulative revenue per customer; each invoice as % of customer total |
| `AVG() OVER()` | Country price benchmark vs global; running avg invoice value; 3-invoice moving average | Country + global avg price; running avg with above/below flag; 3-invoice moving avg |
| `COUNT() OVER()` | Total invoice rows per customer; running row counter; NULL-aware % identified per country | Country + global row count; running row seq per customer; % identified customers per country |
| `MIN() OVER()` | Cheapest price per country; running minimum spend; earliest purchase date per customer | Country + global min price; running minimum revenue; first purchase date + days elapsed (STRPTIME) |
| `MAX() OVER()` | Priciest product per country; personal-best invoice tracker with flag; peak quantity per product | Country + global max price; running max + new-record flag; latest purchase date + days remaining (STRPTIME) |

#### How the exercise system works
- Each exercise file in `exercises/` has a `user_sql_N` placeholder
- Running the file prints `✅ PASS` or `❌ FAIL` with a descriptive message and hint
- If stuck: check the matching file in `solutions/` — same validator, complete SQL included
- ⚠️ Note: MIN/MAX Ex3 intentionally uses STRPTIME to parse InvoiceDate before applying MIN/MAX (string ordering gives wrong results)
- All 15 exercise SQL solutions verified before clearing: 15/15 ✅
- All 15 solutions verified: `python aggregate_functions/solutions/*.py` → 15/15 ✅

---

### ✅ Phase 5 — Distribution / Statistical Functions Tutorial (`distribution_functions/`)

A complete tutorial + exercise system for the three SQL distribution / statistical
window functions, following the same structure as previous modules.

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
└── README.md             # User guide
```

#### Content per function (3 tutorials + 3 exercises each)

| Function | Tutorial Topics | Exercise Topics |
|---|---|---|
| `NTILE()` | Country revenue quartiles; per-country product price deciles; customer spend quintiles with tier labels (Bronze → Diamond) | Countries into qty quartiles; top-quintile customers by spend; per-country product price tiers (Budget / Mid-Range / Premium) |
| `CUME_DIST()` | Country revenue cumulative distribution; per-country product price CUME_DIST; CUME_DIST vs PERCENT_RANK side-by-side | Country revenue cume_dist; customers in top 20% by spend (cume_dist ≥ 0.8); flag bottom-25% cheapest products per country |
| `PERCENT_RANK()` | Customer spend percent rank globally; per-country product price percent rank; NTILE + CUME_DIST + PERCENT_RANK all three side-by-side | Country percent rank by order count; customer spend pct_rank within modal country (using DuckDB MODE()); all three distribution functions side-by-side |

#### How the exercise system works
- Each exercise file in `exercises/` has a `user_sql_N` placeholder
- Running the file prints `✅ PASS` or `❌ FAIL` with a descriptive message and hint
- If stuck: check the matching file in `solutions/` — same validator, complete SQL included
- All 9 exercise SQL solutions verified before clearing: 9/9 ✅
- All 9 solutions verified: `python distribution_functions/solutions/*.py` → 9/9 ✅

---

## Planned / Todo

- [x] **Phase 5 — Distribution / Statistical functions** ✅
  - [x] `NTILE()`, `CUME_DIST()`, `PERCENT_RANK()`
- [x] **Phase 6 — Interview prep** ✅
  - [x] Create 20 concrete advanced SQL questions based on the dataset schema in `interview_questions/questions.md`
  - [x] Create corresponding correctly structured SQL solutions in `interview_questions/solutions/solutions.md`
  - [x] Write an automated `verify_all.py` test script to validate all 20 advanced SQL query solutions against the DuckDB schema
  - [x] Handcrafted `interview_questions/exercises/` directory populated with 20 individual Python files, each containing a placeholder for the SQL query and a textual hint.
  - [x] Implemented a validation system in `interview_questions/validators.py` and confirmed that all exercises initially fail.

---

### ✅ Feature — Solutions Directories

Added a `solutions/` directory inside each function module. Each solution file:
- Contains the complete, verified SQL for every exercise
- Uses the same `check_exercise()` / `validate_*()` logic as the exercise files
- Includes an explanatory comment above each query explaining the key SQL concept
- Is runnable on its own: `python <module>/solutions/<function>.py`

| Module | Solutions | Status |
|---|---|---|
| `ranking_functions/solutions/` | `row_number.py`, `rank.py`, `dense_rank.py` | 9/9 ✅ |
| `value_functions/solutions/` | `lag.py`, `lead.py`, `first_value.py`, `last_value.py` | 12/12 ✅ |
| `aggregate_functions/solutions/` | `sum.py`, `avg.py`, `count.py`, `min.py`, `max.py` | 15/15 ✅ |
| `distribution_functions/solutions/` | `ntile.py`, `cume_dist.py`, `percent_rank.py` | 9/9 ✅ |

### ✅ Refactor — Shared Validation Logic (Ranking functions)

Extracted all validation logic from `exercises/` and `solutions/` into a central `validators.py` file within the `ranking_functions/` module.
- **Consistency:** Exercises and solutions now share the exact same `validate_exN()` functions.
- **Maintainability:** Validation rules are defined in one place, reducing duplication.
- **Verified:** All 9 ranking exercises and 9 solutions pass using the shared logic.

### ✅ Refactor — Shared Validation Logic (Value functions)

Extracted all validation logic from `exercises/` and `solutions/` into a central `validators.py` file within the `value_functions/` module.
- **Consistency:** Exercises and solutions now share the exact same `validate_lag_exN`, `validate_lead_exN`, etc.
- **Maintainability:** Validation rules are defined in one place, reducing duplication.
- **Verified:** All 12 value function exercises and 12 solutions pass using the shared logic.

### ✅ Refactor — Shared Validation Logic (Aggregate functions)

Extracted all validation logic from `exercises/` and `solutions/` into a central `validators.py` file within the `aggregate_functions/` module.
- **Consistency:** Exercises and solutions now share the exact same `validate_sum_exN`, `validate_avg_exN`, etc.
- **Maintainability:** Validation rules are defined in one place, reducing duplication.
- **Verified:** All 15 aggregate function exercises and 15 solutions pass using the shared logic.

### ✅ Refactor — Shared Validation Logic (Distribution functions)

Extracted all validation logic from `exercises/` and `solutions/` into a central `validators.py` file within the `distribution_functions/` module.
- **Consistency:** Exercises and solutions now share the exact same `validate_ntile_exN`, `validate_cume_dist_exN`, etc.
- **Maintainability:** Validation rules are defined in one place, reducing duplication.
- **Verified:** All 9 distribution function exercises and 9 solutions pass using the shared logic.

## How to Run

```bash
# Activate the virtual environment
source .venv/bin/activate

# ── Ranking Functions ──────────────────────────────────────────────
python ranking_functions/tutorials/row_number.py
python ranking_functions/tutorials/rank.py
python ranking_functions/tutorials/dense_rank.py

python ranking_functions/exercises/row_number.py
python ranking_functions/exercises/rank.py
python ranking_functions/exercises/dense_rank.py

# Stuck? Check the solutions
python ranking_functions/solutions/row_number.py
python ranking_functions/solutions/rank.py
python ranking_functions/solutions/dense_rank.py

# Or run everything at once
python ranking_functions/run_all.py

# ── Value Functions ────────────────────────────────────────────────
python value_functions/tutorials/lag.py
python value_functions/tutorials/lead.py
python value_functions/tutorials/first_value.py
python value_functions/tutorials/last_value.py

python value_functions/exercises/lag.py
python value_functions/exercises/lead.py
python value_functions/exercises/first_value.py
python value_functions/exercises/last_value.py

# Stuck? Check the solutions
python value_functions/solutions/lag.py
python value_functions/solutions/lead.py
python value_functions/solutions/first_value.py
python value_functions/solutions/last_value.py

# Or run everything at once
python value_functions/run_all.py

# ── Aggregate Functions ────────────────────────────────────────────
python aggregate_functions/tutorials/sum.py
python aggregate_functions/tutorials/avg.py
python aggregate_functions/tutorials/count.py
python aggregate_functions/tutorials/min.py
python aggregate_functions/tutorials/max.py

python aggregate_functions/exercises/sum.py
python aggregate_functions/exercises/avg.py
python aggregate_functions/exercises/count.py
python aggregate_functions/exercises/min.py
python aggregate_functions/exercises/max.py

# Stuck? Check the solutions
python aggregate_functions/solutions/sum.py
python aggregate_functions/solutions/avg.py
python aggregate_functions/solutions/count.py
python aggregate_functions/solutions/min.py
python aggregate_functions/solutions/max.py

# Or run everything at once
python aggregate_functions/run_all.py

# ── Distribution / Statistical Functions ──────────────────────────────────
python distribution_functions/tutorials/ntile.py
python distribution_functions/tutorials/cume_dist.py
python distribution_functions/tutorials/percent_rank.py

python distribution_functions/exercises/ntile.py
python distribution_functions/exercises/cume_dist.py
python distribution_functions/exercises/percent_rank.py

# Stuck? Check the solutions
python distribution_functions/solutions/ntile.py
python distribution_functions/solutions/cume_dist.py
python distribution_functions/solutions/percent_rank.py

# Or run everything at once
python distribution_functions/run_all.py

# ── Interview Questions ───────────────────────────────────────────────────
# Practice the 20 advanced SQL interview questions
python interview_questions/exercises/01_top_n_records.py
python interview_questions/exercises/02_second_purchase.py
# ... and so on ...
python interview_questions/exercises/20_detect_status_changes.py

# Stuck? Check the solutions in markdown:
# cat interview_questions/solutions/solutions.md
```
