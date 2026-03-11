"""
exercises/dense_rank.py — DENSE_RANK() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/dense_rank.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/dense_rank.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_dense_rank_ex1, validate_dense_rank_ex2, validate_dense_rank_ex3

con = get_connection()

print_header(
    "DENSE_RANK() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Dense rank countries by their total sales value (Quantity * UnitPrice).
# UK should be rank 1. Verify ranks are contiguous (no gaps: 1,2,3,...).
#
# Required columns: Country, total_sales, sales_rank

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: SUM(Quantity * UnitPrice) per Country,
    --       then DENSE_RANK() OVER (ORDER BY total_sales DESC)
"""


user_sql_1 = """
    WITH country_sales AS (
        SELECT 
            Country, 
            SUM(Quantity * UnitPrice) as total_sales 
        FROM retail_data
        WHERE Quantity > 0 
        GROUP BY Country         
    )
    SELECT 
        Country, 
        ROUND(total_sales, 2) as total_sales, 
        DENSE_RANK() OVER(ORDER BY total_sales DESC) sales_rank
    FROM country_sales 
"""





check_exercise(
    number=1,
    description="Dense rank countries by total sales value (contiguous ranks)",
    user_sql=user_sql_1,
    validation_fn=validate_dense_rank_ex1,
    con=con,
    hint="Use DENSE_RANK() — ranks must be 1,2,3,... with no skipped numbers.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Dense rank StockCode by ASCENDING average UnitPrice within each Country.
# The cheapest product per country should get dense rank 1.
#
# Required columns: Country, StockCode, avg_price, price_rank

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: ORDER BY avg_price ASC (cheapest → rank 1)
    -- PARTITION BY Country
"""


user_sql_2 = """
    WITH country_avg AS (
        SELECT 
            Country, 
            StockCode, 
            AVG(UnitPrice) as avg_price 
        FROM retail_data
        WHERE UnitPrice >= 0
        GROUP BY Country, StockCode 
    )
    SELECT 
        Country, 
        StockCode, 
        avg_price,
        DENSE_RANK() OVER(PARTITION BY Country ORDER BY avg_price ASC) as price_rank
    FROM country_avg 
"""


check_exercise(
    number=2,
    description="Dense rank StockCodes by avg UnitPrice ASC within each Country (cheapest = rank 1)",
    user_sql=user_sql_2,
    validation_fn=validate_dense_rank_ex2,
    con=con,
    hint="Use ORDER BY avg_price ASC so the cheapest gets rank 1.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# For the top 15 products sold in Germany (by number of unique orders they
# appear in), compute ROW_NUMBER, RANK, and DENSE_RANK — all in one query,
# all ordered by num_orders DESC.
#
# Because many products appear in the same number of orders, there will be
# natural ties. Watch how:
#   - rn        : always unique (1,2,3,...15)
#   - cust_rank : SKIPS a number after a tie  (e.g. 4,4,6,...)
#   - dense_cust: NEVER skips              (e.g. 4,4,5,...)
#
# Filter: Country = 'Germany', Quantity > 0
# Required columns: StockCode, num_orders, rn, cust_rank, dense_cust
# Return exactly 15 rows (LIMIT 15).

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: COUNT(DISTINCT InvoiceNo) per StockCode WHERE Country = 'Germany' AND Quantity > 0
    -- Then apply all three window fns OVER (ORDER BY num_orders DESC)
    -- Wrap in a CTE and LIMIT 15
"""


user_sql_3 = """
    WITH german_orders AS (
        SELECT 
            StockCode, 
            COUNT(DISTINCT InvoiceNo) as num_orders
        FROM retail_data 
        WHERE Country = 'Germany' AND Quantity > 0 
        GROUP BY StockCode
    )
    SELECT 
        StockCode, 
        num_orders, 
        ROW_NUMBER() OVER(ORDER BY num_orders DESC) as rn, 
        RANK() OVER(ORDER BY num_orders DESC) as cust_rank, 
        DENSE_RANK() OVER(ORDER BY num_orders DESC) as dense_cust
    FROM german_orders 
    LIMIT 15 
"""



check_exercise(
    number=3,
    description="Top-15 Germany products: ROW_NUMBER, RANK, DENSE_RANK side-by-side (forced ties)",
    user_sql=user_sql_3,
    validation_fn=validate_dense_rank_ex3,
    con=con,
    hint=(
        "COUNT(DISTINCT InvoiceNo) per StockCode WHERE Country = 'Germany' AND Quantity > 0. "
        "Apply all three window fns OVER (ORDER BY num_orders DESC), LIMIT 15."
    ),
)
