"""
solutions/sum.py — SUM() OVER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the SUM() OVER() exercises.
Refer to this file ONLY if you are stuck on exercises/sum.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_sum_ex1, validate_sum_ex2, validate_sum_ex3

con = get_connection()

print_header(
    "SUM() OVER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, compute the total revenue for the entire dataset
# (grand_total) and the total revenue for the row's country (country_total).
#
# Key idea: SUM() OVER (PARTITION BY Country) aggregates within each country;
#           SUM() OVER () with NO partition clause spans the entire dataset.

user_sql_1 = """
    SELECT
        Country,
        InvoiceNo,
        StockCode,
        Quantity * UnitPrice AS line_revenue,
        SUM(Quantity * UnitPrice) OVER (PARTITION BY Country) AS country_total,
        SUM(Quantity * UnitPrice) OVER ()                     AS grand_total
    FROM retail_data
    WHERE Quantity > 0 AND UnitPrice > 0
"""




check_exercise(
    number=1,
    description="Total revenue per country and grand total on every row",
    user_sql=user_sql_1,
    validation_fn=validate_sum_ex1,
    con=con,
    hint="SUM(Quantity * UnitPrice) OVER (PARTITION BY Country) and SUM(Quantity * UnitPrice) OVER () for the grand total",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Using invoice-level revenue, compute a running cumulative revenue per customer.
#
# Key idea: aggregate revenue per invoice in a CTE, then use
#           SUM(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
#           which defaults to ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW.

user_sql_2 = """
    WITH invoice_revenue AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            SUM(Quantity * UnitPrice) AS invoice_revenue
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID, InvoiceDate, InvoiceNo
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        invoice_revenue,
        SUM(invoice_revenue) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
        ) AS cumulative_revenue
    FROM invoice_revenue
"""




check_exercise(
    number=2,
    description="Running cumulative revenue per customer ordered by date",
    user_sql=user_sql_2,
    validation_fn=validate_sum_ex2,
    con=con,
    hint="CTE: aggregate SUM(Quantity*UnitPrice) per invoice; then SUM(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each customer invoice, compute what percentage of the customer's
# ALL-TIME revenue this single invoice represents.
#
# Key idea: Two-CTE approach:
#   (1) aggregate invoice revenue per invoice row;
#   (2) add customer_total with SUM() OVER (PARTITION BY CustomerID) — no ORDER BY
#       (we want the total, not a running sum).
#   Then divide and multiply by 100 in the final SELECT.

user_sql_3 = """
    WITH invoice_totals AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            SUM(Quantity * UnitPrice) AS invoice_revenue
        FROM retail_data
        WHERE CustomerID IS NOT NULL AND Quantity > 0
        GROUP BY CustomerID, InvoiceDate, InvoiceNo
    ), with_totals AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            invoice_revenue,
            SUM(invoice_revenue) OVER (PARTITION BY CustomerID) AS customer_total
        FROM invoice_totals
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        invoice_revenue,
        customer_total,
        ROUND(100.0 * invoice_revenue / customer_total, 1) AS pct_of_total
    FROM with_totals
    WHERE customer_total > 0
"""




check_exercise(
    number=3,
    description="Each invoice as a percentage of the customer's all-time revenue",
    user_sql=user_sql_3,
    validation_fn=validate_sum_ex3,
    con=con,
    hint=(
        "Two-CTE approach: (1) invoice_totals — SUM(Quantity*UnitPrice) per invoice; "
        "(2) with_totals — add SUM(invoice_revenue) OVER (PARTITION BY CustomerID) as customer_total; "
        "final SELECT: WHERE customer_total > 0, then ROUND(100.0 * invoice_revenue / customer_total, 1) as pct_of_total."
    ),
)
