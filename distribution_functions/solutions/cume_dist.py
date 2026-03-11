"""
solutions/cume_dist.py — CUME_DIST() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the CUME_DIST() exercises.
Refer to this file ONLY if you are stuck on exercises/cume_dist.py.

Running this file will verify all three solutions pass.
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
    "CUME_DIST() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Cumulative distribution of country revenue across all countries.
#
# Key idea: aggregate per country in a CTE, then CUME_DIST() OVER
# (ORDER BY country_revenue ASC) gives the fraction of countries with
# revenue at or below each country's total. No PARTITION BY = global ranking.

user_sql_1 = """
    WITH country_rev AS (
        SELECT
            Country,
            ROUND(SUM(Quantity * UnitPrice), 2) AS country_revenue
        FROM retail_data
        WHERE Quantity > 0
        GROUP BY Country
    )
    SELECT
        Country,
        country_revenue,
        ROUND(CUME_DIST() OVER (ORDER BY country_revenue ASC), 4) AS cume_dist
    FROM country_rev
    ORDER BY country_revenue ASC
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
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Customers whose total spend is in the top 20 % (cume_dist >= 0.8).
#
# Key idea: compute CUME_DIST in a CTE or subquery, then filter in an
# outer SELECT. You cannot use a window function directly in a WHERE clause.

user_sql_2 = """
    WITH customer_spend AS (
        SELECT
            CustomerID,
            ROUND(SUM(Quantity * UnitPrice), 2) AS total_spend
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID
    ), with_cume AS (
        SELECT
            CustomerID,
            total_spend,
            ROUND(CUME_DIST() OVER (ORDER BY total_spend ASC), 4) AS cume_dist
        FROM customer_spend
    )
    SELECT
        CustomerID,
        total_spend,
        cume_dist
    FROM with_cume
    WHERE cume_dist >= 0.8
    ORDER BY total_spend DESC
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
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Flag bottom-25% cheapest products per country using cume_dist <= 0.25.
#
# Key idea: PARTITION BY Country resets CUME_DIST independently per country.
# A CASE (or boolean expression) then flags rows where cume_dist <= 0.25.

user_sql_3 = """
    WITH product_prices AS (
        SELECT
            Country,
            StockCode,
            ROUND(AVG(UnitPrice), 2) AS avg_price
        FROM retail_data
        WHERE Quantity > 0 AND UnitPrice > 0
        GROUP BY Country, StockCode
    ), with_cume AS (
        SELECT
            Country,
            StockCode,
            avg_price,
            ROUND(
                CUME_DIST() OVER (
                    PARTITION BY Country
                    ORDER BY avg_price ASC
                ), 4
            ) AS cume_dist
        FROM product_prices
        WHERE Country IN ('United Kingdom', 'Germany', 'France')
    )
    SELECT
        Country,
        StockCode,
        avg_price,
        cume_dist,
        CASE WHEN cume_dist <= 0.25 THEN TRUE ELSE FALSE END AS is_cheap
    FROM with_cume
    ORDER BY Country, avg_price ASC
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
