"""
solutions/percent_rank.py — PERCENT_RANK() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the PERCENT_RANK() exercises.
Refer to this file ONLY if you are stuck on exercises/percent_rank.py.

Running this file will verify all three solutions pass.
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
    "PERCENT_RANK() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Percent rank of countries by order count.
#
# Key idea: COUNT(DISTINCT InvoiceNo) gives the number of unique orders per
# country. PERCENT_RANK() OVER (ORDER BY order_count ASC) then maps ranks
# to [0, 1]. The country with the fewest orders always gets 0.0.

user_sql_1 = """
    WITH country_orders AS (
        SELECT
            Country,
            COUNT(DISTINCT InvoiceNo) AS order_count
        FROM retail_data
        WHERE Quantity > 0
        GROUP BY Country
    )
    SELECT
        Country,
        order_count,
        ROUND(PERCENT_RANK() OVER (ORDER BY order_count ASC), 4) AS pct_rank
    FROM country_orders
    ORDER BY order_count ASC
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
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Customer spend percent rank within their modal country.
#
# Key idea: MODE() is an aggregate function in DuckDB that returns the most
# frequent value in a group — the perfect tool for "modal country".
# After computing modal_country and total_spend per customer, partition
# PERCENT_RANK by modal_country to rank customers within their most-visited
# country.

user_sql_2 = """
    WITH customer_stats AS (
        SELECT
            CustomerID,
            MODE(Country)                          AS modal_country,
            ROUND(SUM(Quantity * UnitPrice), 2)    AS total_spend
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID
    )
    SELECT
        CustomerID,
        modal_country,
        total_spend,
        ROUND(
            PERCENT_RANK() OVER (
                PARTITION BY modal_country
                ORDER BY total_spend ASC
            ), 4
        ) AS pct_rank
    FROM customer_stats
    ORDER BY modal_country, total_spend ASC
    LIMIT 30
"""




check_exercise(
    number=2,
    description="Customer spend percent rank within their modal country",
    user_sql=user_sql_2,
    validation_fn=validate_percent_rank_ex2,
    con=con,
    hint=(
        "CTE: aggregate total_spend per CustomerID and find modal_country with "
        "MODE() aggregate on Country grouped by CustomerID; "
        "CTE2 or inline: ROUND(PERCENT_RANK() OVER (PARTITION BY modal_country "
        "ORDER BY total_spend ASC), 4) AS pct_rank; "
        "Simplest approach: use MODE() aggregate on Country grouped by CustomerID."
    ),
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# All three distribution functions side-by-side on customer spend.
#
# Key idea: aggregate in a single CTE, then compute NTILE, CUME_DIST, and
# PERCENT_RANK in three separate window expressions in the final SELECT.
# All three share the same ORDER BY total_spend ASC — no PARTITION BY means
# they all operate globally across the full customer set.

user_sql_3 = """
    WITH customer_spend AS (
        SELECT
            CustomerID,
            ROUND(SUM(Quantity * UnitPrice), 2) AS total_spend
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID
    )
    SELECT
        CustomerID,
        total_spend,
        NTILE(4)       OVER (ORDER BY total_spend ASC)        AS ntile_quartile,
        ROUND(CUME_DIST()    OVER (ORDER BY total_spend ASC), 4) AS cume_dist,
        ROUND(PERCENT_RANK() OVER (ORDER BY total_spend ASC), 4) AS pct_rank
    FROM customer_spend
    ORDER BY total_spend ASC
    LIMIT 25
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
