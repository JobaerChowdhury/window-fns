"""
exercises/ntile.py — NTILE() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/ntile.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/ntile.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import (
    validate_ntile_ex1,
    validate_ntile_ex2,
    validate_ntile_ex3,
)

con = get_connection()

print_header(
    "NTILE() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Compute the total quantity sold per country (only Quantity > 0).
# Then assign each country to one of 4 quartiles based on total_qty ASC.
# Required columns: Country, total_qty, qty_quartile
# Order the final result by qty_quartile, total_qty.

user_sql_1 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=1,
    description="Assign countries to revenue quartiles by total quantity sold",
    user_sql=user_sql_1,
    validation_fn=validate_ntile_ex1,
    con=con,
    hint="CTE: SUM(Quantity) GROUP BY Country WHERE Quantity > 0; then NTILE(4) OVER (ORDER BY total_qty ASC).",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# For each customer, compute their total spend (Quantity > 0, CustomerID
# IS NOT NULL). Assign each customer to one of 5 spend quintiles (1 = lowest).
# Then filter to only the TOP quintile (quintile 5) customers.
# Required columns: CustomerID, total_spend, spend_quintile
# Order by total_spend DESC.

user_sql_2 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=2,
    description="Top-quintile customers by total spend",
    user_sql=user_sql_2,
    validation_fn=validate_ntile_ex2,
    con=con,
    hint=(
        "CTE: SUM(Quantity * UnitPrice) per CustomerID (filter Quantity > 0 and CustomerID IS NOT NULL); "
        "then NTILE(5) OVER (ORDER BY total_spend ASC) as spend_quintile; "
        "final SELECT: WHERE spend_quintile = 5."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For each country, assign products (StockCode) into 3 price tiers based on
# their average UnitPrice within that country (ASC order).
# Tier 1 = cheapest third, Tier 3 = most expensive third.
# Use a CASE expression to label tiers: 'Budget', 'Mid-Range', 'Premium'.
# Required columns: Country, StockCode, avg_price, price_tier, tier_label
# Only include Quantity > 0 and UnitPrice > 0.
# Order by Country, avg_price.

user_sql_3 = """
    -- YOUR SQL HERE
"""




check_exercise(
    number=3,
    description="Per-country product price tiers (Budget / Mid-Range / Premium)",
    user_sql=user_sql_3,
    validation_fn=validate_ntile_ex3,
    con=con,
    hint=(
        "CTE: AVG(UnitPrice) GROUP BY Country, StockCode (filter Quantity > 0 AND UnitPrice > 0); "
        "then NTILE(3) OVER (PARTITION BY Country ORDER BY avg_price ASC) AS price_tier; "
        "CASE price_tier WHEN 1 THEN 'Budget' WHEN 2 THEN 'Mid-Range' ELSE 'Premium' END AS tier_label."
    ),
)
