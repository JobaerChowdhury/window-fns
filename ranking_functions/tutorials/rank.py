"""
tutorials/rank.py — RANK() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RANK() assigns the same rank to rows with equal sort values (ties), then
SKIPS ranks to account for the tie. If three rows share rank 2, the next
rank is 5 — there is a "gap".

Syntax:
    RANK() OVER ([PARTITION BY col, ...] ORDER BY col [ASC|DESC])

Key difference vs ROW_NUMBER():
    - ROW_NUMBER: always unique, no ties  → 1, 2, 3, 4, 5
    - RANK      : ties share a rank, gaps → 1, 2, 2, 4, 5

Run this file:
    python tutorials/rank.py

Then head to exercises/rank.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "RANK() — Ranking With Gaps on Ties",
    "RANK() gives tied rows the same rank number, then jumps ahead by the "
    "number of tied rows. This mirrors how sports competitions are ranked: "
    "if two athletes tie for 2nd, the next rank is 4th.",
)


# ── Tutorial 1: Rank all products by total quantity sold ─────────────────────
run_tutorial(
    title="Rank all products by total quantity sold (global)",
    description=(
        "Aggregate total quantity per StockCode, then apply RANK() ordered by "
        "total_qty DESC. Products with the same total quantity share a rank, "
        "and the next rank skips accordingly."
    ),
    sql="""
        WITH product_totals AS (
            SELECT
                StockCode,
                Description,
                SUM(Quantity) AS total_qty
            FROM retail_data
            WHERE Quantity > 0
            GROUP BY StockCode, Description
        )
        SELECT
            RANK() OVER (ORDER BY total_qty DESC)  AS qty_rank,
            StockCode,
            Description,
            total_qty
        FROM product_totals
        ORDER BY qty_rank
        LIMIT 20
    """,
    con=con,
)

# ── Tutorial 2: Rank customers by total spend within each country ─────────────
run_tutorial(
    title="Rank customers by total spend within their country",
    description=(
        "PARTITION BY Country resets the rank counter for each country. "
        "Rank 1 in Germany is the top spender in Germany — completely "
        "independent of rank 1 in France."
    ),
    sql="""
        WITH customer_spend AS (
            SELECT
                CustomerID,
                Country,
                SUM(Quantity * UnitPrice) AS total_spend
            FROM retail_data
            WHERE CustomerID IS NOT NULL
              AND Quantity > 0
            GROUP BY CustomerID, Country
        )
        SELECT
            Country,
            CustomerID,
            total_spend,
            RANK() OVER (
                PARTITION BY Country
                ORDER BY total_spend DESC
            ) AS spend_rank
        FROM customer_spend
        ORDER BY Country, spend_rank
        LIMIT 25
    """,
    con=con,
)

# ── Tutorial 3: Demonstrate the gap — RANK vs ROW_NUMBER side by side ─────────
run_tutorial(
    title="See the gap: RANK vs ROW_NUMBER on tied values",
    description=(
        "This query shows both functions on the same data so you can see "
        "exactly where RANK() creates gaps while ROW_NUMBER() does not. "
        "Notice rows that share a RANK value always have consecutive "
        "ROW_NUMBER values."
    ),
    sql="""
        WITH daily_sales AS (
            SELECT
                Country,
                strptime(InvoiceDate, '%m/%d/%Y %H:%M')::DATE AS sale_date,
                SUM(Quantity * UnitPrice) AS daily_revenue
            FROM retail_data
            WHERE Country IN ('Germany', 'France', 'Spain')
              AND Quantity > 0
            GROUP BY Country, strptime(InvoiceDate, '%m/%d/%Y %H:%M')::DATE
        )
        SELECT
            Country,
            sale_date,
            daily_revenue,
            RANK()       OVER (PARTITION BY Country ORDER BY daily_revenue DESC) AS rank_val,
            ROW_NUMBER() OVER (PARTITION BY Country ORDER BY daily_revenue DESC) AS row_num
        FROM daily_sales
        ORDER BY Country, rank_val
        LIMIT 30
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/rank.py\n")
