"""
solutions/dense_rank.py — DENSE_RANK() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the DENSE_RANK() exercises.
Refer to this file ONLY if you are stuck on exercises/dense_rank.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_dense_rank_ex1, validate_dense_rank_ex2, validate_dense_rank_ex3

con = get_connection()

print_header(
    "DENSE_RANK() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Dense rank countries by their total sales value (Quantity * UnitPrice).
#
# Key idea: DENSE_RANK() produces contiguous integers (1, 2, 3, …) with no
#           gaps, unlike RANK() which skips numbers after ties.

user_sql_1 = """
    WITH country_sales AS (
        SELECT
            Country,
            SUM(Quantity * UnitPrice) AS total_sales
        FROM retail_data
        WHERE Quantity > 0
        GROUP BY Country
    )
    SELECT
        Country,
        ROUND(total_sales, 2) AS total_sales,
        DENSE_RANK() OVER (ORDER BY total_sales DESC) AS sales_rank
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
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Dense rank StockCode by ASCENDING average UnitPrice within each Country.
# The cheapest product per country should get dense rank 1.
#
# Key idea: ORDER BY avg_price ASC so the lowest price becomes rank 1.
#           PARTITION BY Country so each country gets its own rank sequence.

user_sql_2 = """
    WITH country_avg AS (
        SELECT
            Country,
            StockCode,
            AVG(UnitPrice) AS avg_price
        FROM retail_data
        WHERE UnitPrice >= 0
        GROUP BY Country, StockCode
    )
    SELECT
        Country,
        StockCode,
        avg_price,
        DENSE_RANK() OVER (PARTITION BY Country ORDER BY avg_price ASC) AS price_rank
    FROM country_avg
"""


def validate_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "price_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    rank1 = df[df["price_rank"] == 1]
    min_price = df.groupby("country")["avg_price"].min().reset_index().rename(columns={"avg_price": "min_price"})
    merged = rank1.merge(min_price, on="country")
    if not (merged["avg_price"] <= merged["min_price"] * 1.001).all():
        return False, "Rank 1 does not correspond to the lowest avg_price per country — check ORDER BY direction (ASC)."
    return True, f"Rank 1 correctly identifies the cheapest product per country across {df['country'].nunique()} countries."


check_exercise(
    number=2,
    description="Dense rank StockCodes by avg UnitPrice ASC within each Country (cheapest = rank 1)",
    user_sql=user_sql_2,
    validation_fn=validate_dense_rank_ex2,
    con=con,
    hint="Use ORDER BY avg_price ASC so the cheapest gets rank 1.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Top-15 Germany products by order count: ROW_NUMBER, RANK, DENSE_RANK side-by-side.
#
# Key idea: COUNT(DISTINCT InvoiceNo) is a small integer — many products
# share the same count, creating natural ties. This makes the difference
# between the three functions unmissable:
#   - rn        : 1,2,3,...15 — always unique, no gaps, no ties
#   - cust_rank : SKIPS a number after a tie (e.g. 4,4 → next is 6, not 5)
#   - dense_cust: NEVER skips              (e.g. 4,4 → next is 5)

user_sql_3 = """
    WITH germany_products AS (
        SELECT
            StockCode,
            COUNT(DISTINCT InvoiceNo) AS num_orders
        FROM retail_data
        WHERE Country = 'Germany' AND Quantity > 0
        GROUP BY StockCode
    )
    SELECT
        StockCode,
        num_orders,
        ROW_NUMBER() OVER (ORDER BY num_orders DESC) AS rn,
        RANK()       OVER (ORDER BY num_orders DESC) AS cust_rank,
        DENSE_RANK() OVER (ORDER BY num_orders DESC) AS dense_cust
    FROM germany_products
    ORDER BY num_orders DESC
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
