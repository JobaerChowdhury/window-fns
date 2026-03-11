"""
exercises/rank.py — RANK() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/rank.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/rank.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_rank_ex1, validate_rank_ex2, validate_rank_ex3

con = get_connection()

print_header(
    "RANK() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Rank countries by the number of unique customers.
# United Kingdom should be rank 1.
#
# Required columns: Country, unique_customers, country_rank

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: COUNT(DISTINCT CustomerID) per Country, then RANK() by that count DESC
"""


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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Rank each StockCode by its average UnitPrice, within each Country.
# No rank value should exceed the number of rows in its partition.
#
# Required columns: Country, StockCode, avg_price, price_rank

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: aggregate AVG(UnitPrice) per (Country, StockCode),
    --       then RANK() OVER (PARTITION BY Country ORDER BY avg_price DESC)
"""


user_sql_2 = """
    WITH avg_prices AS (
        SELECT
            Country,
            StockCode, 
            AVG(UnitPrice) AS avg_price, 
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For the top 15 products sold in France (by total Quantity), compute
# ROW_NUMBER, RANK, and DENSE_RANK — all in one query, all ordered by
# total_qty DESC.  Ties will get the same pos_rank / dense_pos, but a
# unique rn.  Notice where pos_rank SKIPS a number but dense_pos does not.
#
# Filter: Country = 'France', Quantity > 0
# Required columns: StockCode, total_qty, rn, pos_rank, dense_pos
# Return exactly 15 rows (use LIMIT 15 in the outer query).

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: SUM(Quantity) per StockCode WHERE Country = 'France' AND Quantity > 0
    -- Then apply all three functions OVER (ORDER BY total_qty DESC) in one SELECT
    -- Wrap in a CTE and LIMIT 15
"""


user_sql_3 = """
    WITH product_qty AS (
        SELECT 
            StockCode, 
            SUM(Quantity) as total_qty
        FROM retail_data
        WHERE Country = 'France' AND Quantity > 0
        GROUP BY StockCode

    )
    SELECT 
        StockCode, 
        total_qty, 
        ROW_NUMBER() OVER(ORDER BY total_qty DESC) as rn, 
        RANK() OVER(ORDER BY total_qty DESC) as pos_rank, 
        DENSE_RANK() OVER(ORDER BY total_qty DESC) as dense_pos
    FROM product_qty 
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
