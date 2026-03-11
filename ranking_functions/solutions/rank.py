"""
solutions/rank.py — RANK() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the RANK() exercises.
Refer to this file ONLY if you are stuck on exercises/rank.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_rank_ex1, validate_rank_ex2, validate_rank_ex3

con = get_connection()

print_header(
    "RANK() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Rank countries by the number of unique customers.
#
# Key idea: aggregate unique customers in a CTE first, then apply RANK() in
#           the outer query over the whole result set (no PARTITION BY).

user_sql_1 = """
    WITH customer_counts AS (
        SELECT
            Country,
            COUNT(DISTINCT CustomerID) AS unique_customers
        FROM retail_data
        GROUP BY Country
    )
    SELECT
        Country,
        unique_customers,
        RANK() OVER (ORDER BY unique_customers DESC) AS country_rank
    FROM customer_counts
"""




check_exercise(
    number=1,
    description="Rank countries by number of unique customers",
    user_sql=user_sql_1,
    validation_fn=validate_rank_ex1,
    con=con,
    hint="COUNT(DISTINCT CustomerID) then RANK() OVER (ORDER BY ... DESC)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Rank each StockCode by its average UnitPrice, within each Country.
#
# Key idea: aggregate AVG(UnitPrice) per (Country, StockCode) in a CTE,
#           then RANK() OVER (PARTITION BY Country ORDER BY avg_price DESC).

user_sql_2 = """
    WITH avg_prices AS (
        SELECT
            Country,
            StockCode,
            AVG(UnitPrice) AS avg_price
        FROM retail_data
        GROUP BY Country, StockCode
    )
    SELECT
        Country,
        StockCode,
        avg_price,
        RANK() OVER (PARTITION BY Country ORDER BY avg_price DESC) AS price_rank
    FROM avg_prices
"""




check_exercise(
    number=2,
    description="Rank StockCodes by average UnitPrice within each Country",
    user_sql=user_sql_2,
    validation_fn=validate_rank_ex2,
    con=con,
    hint="AVG(UnitPrice) grouped by (Country, StockCode), then RANK() OVER (PARTITION BY Country ORDER BY avg_price DESC)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Top-15 France products: ROW_NUMBER, RANK, DENSE_RANK side-by-side.
#
# Key idea: with 15 rows you can clearly SEE the difference:
#   - ROW_NUMBER (rn)    : always 1,2,3,...15 — no ties, no gaps
#   - RANK     (pos_rank): skips numbers after ties  (e.g. 1,1,3,...)
#   - DENSE_RANK(dense_pos): never skips, stays contiguous (e.g. 1,1,2,...)

user_sql_3 = """
    WITH france_qty AS (
        SELECT
            StockCode,
            SUM(Quantity) AS total_qty
        FROM retail_data
        WHERE Country = 'France' AND Quantity > 0
        GROUP BY StockCode
    )
    SELECT
        StockCode,
        total_qty,
        ROW_NUMBER() OVER (ORDER BY total_qty DESC) AS rn,
        RANK()       OVER (ORDER BY total_qty DESC) AS pos_rank,
        DENSE_RANK() OVER (ORDER BY total_qty DESC) AS dense_pos
    FROM france_qty
    ORDER BY total_qty DESC
    LIMIT 15
"""




check_exercise(
    number=3,
    description="Top-15 France products: ROW_NUMBER, RANK, DENSE_RANK side-by-side",
    user_sql=user_sql_3,
    validation_fn=validate_rank_ex3,
    con=con,
    hint="Use one CTE that aggregates SUM(Quantity) for France, then SELECT with all three window fns OVER (ORDER BY total_qty DESC), LIMIT 15.",
)
