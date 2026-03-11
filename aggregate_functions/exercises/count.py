"""
exercises/count.py — COUNT() OVER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/count.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/count.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_count_ex1, validate_count_ex2, validate_count_ex3

con = get_connection()

print_header(
    "COUNT() OVER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For every row, attach the total number of *rows* in that country
# (country_row_count) and the total number of rows in the whole dataset
# (global_row_count).
# Required columns: Country, InvoiceNo, StockCode,
#                   country_row_count, global_row_count

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Row count per country and total row count on every row",
    user_sql=user_sql_1,
    validation_fn=validate_count_ex1,
    con=con,
    hint="COUNT(*) OVER (PARTITION BY Country) and COUNT(*) OVER () for the global count",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# For each customer, compute a running count of invoice line-item rows
# ordered by InvoiceDate (how many rows have been processed so far).
# Required columns: CustomerID, InvoiceDate, InvoiceNo, StockCode, row_seq
# Only include CustomerID IS NOT NULL.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Running row counter per customer ordered by InvoiceDate",
    user_sql=user_sql_2,
    validation_fn=validate_count_ex2,
    con=con,
    hint="COUNT(*) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS row_seq",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For every row, compute the number of rows where CustomerID IS NOT NULL
# in the same Country (identified_rows) and the total rows in that Country
# (total_rows). Use these to derive pct_identified (rounded to 1 decimal).
# Required columns: Country, InvoiceNo, CustomerID,
#                   identified_rows, total_rows, pct_identified

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="Identified customer percentage per country on every row",
    user_sql=user_sql_3,
    validation_fn=validate_count_ex3,
    con=con,
    hint="COUNT(CustomerID) OVER (PARTITION BY Country) for non-NULLs; COUNT(*) OVER (PARTITION BY Country) for total; divide and multiply by 100",
)
