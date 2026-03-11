"""
solutions/ntile.py — NTILE() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the NTILE() exercises.
Refer to this file ONLY if you are stuck on exercises/ntile.py.

Running this file will verify all three solutions pass.
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
    "NTILE() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Compute the total quantity sold per country and assign each country
# to one of 4 quartiles.
#
# Key idea: aggregate in a CTE, then apply NTILE(4) OVER (ORDER BY total_qty ASC)
# in the outer SELECT. No PARTITION BY needed — we want a global ranking.

user_sql_1 = """
    WITH country_qty AS (
        SELECT
            Country,
            SUM(Quantity) AS total_qty
        FROM retail_data
        WHERE Quantity > 0
        GROUP BY Country
    )
    SELECT
        Country,
        total_qty,
        NTILE(4) OVER (ORDER BY total_qty ASC) AS qty_quartile
    FROM country_qty
    ORDER BY qty_quartile, total_qty
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
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Identify top-quintile (quintile = 5) customers by total spend.
#
# Key idea: aggregate in a CTE, apply NTILE(5) OVER (ORDER BY total_spend ASC),
# then filter WHERE spend_quintile = 5 to keep only the top 20%.

user_sql_2 = """
    WITH customer_spend AS (
        SELECT
            CustomerID,
            ROUND(SUM(Quantity * UnitPrice), 2) AS total_spend
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID
    ), with_quintile AS (
        SELECT
            CustomerID,
            total_spend,
            NTILE(5) OVER (ORDER BY total_spend ASC) AS spend_quintile
        FROM customer_spend
    )
    SELECT
        CustomerID,
        total_spend,
        spend_quintile
    FROM with_quintile
    WHERE spend_quintile = 5
    ORDER BY total_spend DESC
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
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Assign products within each country to 3 price tiers with descriptive labels.
#
# Key idea: PARTITION BY Country in the NTILE window resets the 1–3 bucket
# assignment independently for each country. A CASE expression then maps
# bucket numbers directly to human-readable tier labels.

user_sql_3 = """
    WITH product_prices AS (
        SELECT
            Country,
            StockCode,
            ROUND(AVG(UnitPrice), 2) AS avg_price
        FROM retail_data
        WHERE Quantity > 0 AND UnitPrice > 0
        GROUP BY Country, StockCode
    )
    SELECT
        Country,
        StockCode,
        avg_price,
        NTILE(3) OVER (
            PARTITION BY Country
            ORDER BY avg_price ASC
        ) AS price_tier,
        CASE NTILE(3) OVER (PARTITION BY Country ORDER BY avg_price ASC)
            WHEN 1 THEN 'Budget'
            WHEN 2 THEN 'Mid-Range'
            ELSE        'Premium'
        END AS tier_label
    FROM product_prices
    ORDER BY Country, avg_price
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
