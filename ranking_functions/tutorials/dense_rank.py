"""
tutorials/dense_rank.py — DENSE_RANK() Tutorials
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DENSE_RANK() is like RANK() in that tied rows share the same rank — but it
NEVER skips ranks. The next value after a tie is always the previous rank + 1.

Syntax:
    DENSE_RANK() OVER ([PARTITION BY col, ...] ORDER BY col [ASC|DESC])

Comparison table:
  Values:       100, 100, 90, 80, 80, 70
  ROW_NUMBER:     1,   2,  3,  4,  5,  6   ← always unique
  RANK:           1,   1,  3,  4,  4,  6   ← gaps after ties
  DENSE_RANK:     1,   1,  2,  3,  3,  4   ← no gaps

Run this file:
    python tutorials/dense_rank.py

Then head to exercises/dense_rank.py to practice.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, run_tutorial, print_header

con = get_connection()

print_header(
    "DENSE_RANK() — Ranking Without Gaps",
    "DENSE_RANK() assigns the same rank to ties, then increments by 1 for "
    "the next distinct value — no gaps. Use it when you want to say "
    "'top 3 tiers' rather than 'top 3 positions', because rank 3 is always "
    "the third distinct value regardless of how many ties exist above it.",
)


# ── Tutorial 1: Dense rank all products by total revenue ──────────────────────
run_tutorial(
    title="Dense rank products by total revenue (no gaps)",
    description=(
        "Compute total revenue per product (StockCode) and apply DENSE_RANK(). "
        "Even if many products share the same revenue, the next rank is always "
        "the previous rank + 1 — there are no skipped numbers."
    ),
    sql="""
        WITH product_revenue AS (
            SELECT
                StockCode,
                Description,
                SUM(Quantity * UnitPrice) AS total_revenue
            FROM retail_data
            WHERE Quantity > 0
            GROUP BY StockCode, Description
        )
        SELECT
            DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank,
            StockCode,
            Description,
            ROUND(total_revenue, 2) AS total_revenue
        FROM product_revenue
        ORDER BY revenue_rank
        LIMIT 20
    """,
    con=con,
)

# ── Tutorial 2: Dense rank customers by order count within country ────────────
run_tutorial(
    title="Dense rank customers by number of orders within their country",
    description=(
        "PARTITION BY Country creates independent dense rankings per country. "
        "The customer with the most orders in Germany gets dense rank 1 in "
        "Germany, completely unrelated to France's rank 1."
    ),
    sql="""
        WITH customer_orders AS (
            SELECT
                CustomerID,
                Country,
                COUNT(DISTINCT InvoiceNo) AS num_orders
            FROM retail_data
            WHERE CustomerID IS NOT NULL
            GROUP BY CustomerID, Country
        )
        SELECT
            Country,
            CustomerID,
            num_orders,
            DENSE_RANK() OVER (
                PARTITION BY Country
                ORDER BY num_orders DESC
            ) AS order_rank
        FROM customer_orders
        ORDER BY Country, order_rank
        LIMIT 30
    """,
    con=con,
)

# ── Tutorial 3: All three ranking functions side by side ──────────────────────
run_tutorial(
    title="All three ranking functions side by side",
    description=(
        "This is the 'compare all' view. Run all three window functions on "
        "the same data so you can see exactly how they differ. Focus on rows "
        "where the sort value repeats — that's where the functions diverge."
    ),
    sql="""
        WITH daily_qty AS (
            SELECT
                Country,
                strptime(InvoiceDate, '%m/%d/%Y %H:%M')::DATE AS sale_date,
                SUM(Quantity)             AS total_qty
            FROM retail_data
            WHERE Country IN ('Germany', 'France')
              AND Quantity > 0
            GROUP BY Country, strptime(InvoiceDate, '%m/%d/%Y %H:%M')::DATE
        )
        SELECT
            Country,
            sale_date,
            total_qty,
            ROW_NUMBER()  OVER (PARTITION BY Country ORDER BY total_qty DESC) AS row_num,
            RANK()        OVER (PARTITION BY Country ORDER BY total_qty DESC) AS rank_val,
            DENSE_RANK()  OVER (PARTITION BY Country ORDER BY total_qty DESC) AS dense_rank_val
        FROM daily_qty
        ORDER BY Country, dense_rank_val
        LIMIT 30
    """,
    con=con,
)

print("\n  ✅ All tutorials complete. Now try: python exercises/dense_rank.py\n")
