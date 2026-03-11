"""
exercises/cume_dist.py — CUME_DIST() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/cume_dist.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/cume_dist.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import (
    validate_cume_dist_ex1,
    validate_cume_dist_ex2,
    validate_cume_dist_ex3,
)

con = get_connection()

print_header(
    "CUME_DIST() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Compute the cumulative distribution of country revenue across all countries.
# Required columns: Country, country_revenue, cume_dist (rounded to 4 dp)
# Only include Quantity > 0 rows.
# Order by country_revenue ASC.

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Cumulative distribution of country revenue",
    user_sql=user_sql_1,
    validation_fn=validate_cume_dist_ex1,
    con=con,
    hint=(
        "CTE: SUM(Quantity * UnitPrice) GROUP BY Country WHERE Quantity > 0; "
        "then ROUND(CUME_DIST() OVER (ORDER BY country_revenue ASC), 4) AS cume_dist."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Find all customers whose total spend is in the TOP 20% (cume_dist >= 0.8)
# relative to all customers globally.
# Required columns: CustomerID, total_spend, cume_dist (rounded to 4 dp)
# Only CustomerID IS NOT NULL and Quantity > 0.
# Order by total_spend DESC.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Customers in the top 20% of global spend by cume_dist",
    user_sql=user_sql_2,
    validation_fn=validate_cume_dist_ex2,
    con=con,
    hint=(
        "CTE: SUM(Quantity * UnitPrice) per CustomerID (filter Quantity > 0 and CustomerID IS NOT NULL); "
        "then CUME_DIST() OVER (ORDER BY total_spend ASC) as cume_dist; "
        "final SELECT: WHERE cume_dist >= 0.8, ORDER BY total_spend DESC."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each country, compute the cumulative distribution of product avg price
# within that country. Then flag products that are in the BOTTOM 25%
# of their country's price distribution (cume_dist <= 0.25) as 'cheap'.
# Required columns: Country, StockCode, avg_price, cume_dist (4 dp),
#                   is_cheap (True/False boolean)
# Only countries: 'United Kingdom', 'Germany', 'France'.
# Only UnitPrice > 0 and Quantity > 0.
# Order by Country, avg_price ASC.

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="Flag bottom-25% cheapest products per country using cume_dist",
    user_sql=user_sql_3,
    validation_fn=validate_cume_dist_ex3,
    con=con,
    hint=(
        "CTE: AVG(UnitPrice) GROUP BY Country, StockCode (filter Quantity > 0 AND UnitPrice > 0); "
        "then ROUND(CUME_DIST() OVER (PARTITION BY Country ORDER BY avg_price ASC), 4) AS cume_dist; "
        "CASE WHEN cume_dist <= 0.25 THEN TRUE ELSE FALSE END AS is_cheap; "
        "WHERE Country IN ('United Kingdom', 'Germany', 'France')."
    ),
)
