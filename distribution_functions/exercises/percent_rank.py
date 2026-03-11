"""
exercises/percent_rank.py — PERCENT_RANK() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/percent_rank.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/percent_rank.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import (
    validate_percent_rank_ex1,
    validate_percent_rank_ex2,
    validate_percent_rank_ex3,
)

con = get_connection()

print_header(
    "PERCENT_RANK() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Compute the percent rank of each country by its total number of orders
# (distinct InvoiceNo), globally across all countries.
# Required columns: Country, order_count, pct_rank (rounded to 4 dp)
# Only include Quantity > 0.
# Order by order_count ASC.

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Percent rank of countries by order count",
    user_sql=user_sql_1,
    validation_fn=validate_percent_rank_ex1,
    con=con,
    hint=(
        "CTE: COUNT(DISTINCT InvoiceNo) GROUP BY Country WHERE Quantity > 0; "
        "then ROUND(PERCENT_RANK() OVER (ORDER BY order_count ASC), 4) AS pct_rank."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# For each customer, compute their percent rank by total spend within their
# country of first purchase (i.e., partition by the country that appears on
# their first invoice when sorted by InvoiceDate ASC).
#
# Simplification: use the customer's most frequent country instead.
# Compute each customer's modal_country (the country appearing most in their
# transactions), then rank customers by total_spend within modal_country.
#
# Required columns: CustomerID, modal_country, total_spend, pct_rank (4 dp)
# Only CustomerID IS NOT NULL and Quantity > 0.
# Order by modal_country, total_spend ASC.
# Limit to 30 rows.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Customer spend percent rank within their modal country",
    user_sql=user_sql_2,
    validation_fn=validate_percent_rank_ex2,
    con=con,
    hint=(
        "CTE1: aggregate total_spend per CustomerID and find modal_country with "
        "MODE() or a row_number trick on (CustomerID, Country) ordered by count DESC; "
        "CTE2 or inline: ROUND(PERCENT_RANK() OVER (PARTITION BY modal_country "
        "ORDER BY total_spend ASC), 4) AS pct_rank; "
        "Simplest approach: use MODE() aggregate on Country grouped by CustomerID."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# Show all three distribution functions side-by-side for customers ranked
# by their total spend globally (Quantity > 0, CustomerID IS NOT NULL).
# Required columns: CustomerID, total_spend, ntile_quartile (NTILE 4),
#                   cume_dist (4 dp), pct_rank (4 dp)
# Order by total_spend ASC.
# Limit to 25 rows.

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="NTILE(4), CUME_DIST, and PERCENT_RANK side-by-side on customer spend",
    user_sql=user_sql_3,
    validation_fn=validate_percent_rank_ex3,
    con=con,
    hint=(
        "CTE: SUM(Quantity * UnitPrice) per CustomerID (filter Quantity > 0 and CustomerID IS NOT NULL); "
        "then SELECT CustomerID, total_spend, "
        "NTILE(4) OVER (ORDER BY total_spend ASC) AS ntile_quartile, "
        "ROUND(CUME_DIST() OVER (ORDER BY total_spend ASC), 4) AS cume_dist, "
        "ROUND(PERCENT_RANK() OVER (ORDER BY total_spend ASC), 4) AS pct_rank."
    ),
)
