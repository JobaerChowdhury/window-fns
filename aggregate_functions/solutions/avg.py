"""
solutions/avg.py — AVG() OVER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the AVG() OVER() exercises.
Refer to this file ONLY if you are stuck on exercises/avg.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_avg_ex1, validate_avg_ex2, validate_avg_ex3

con = get_connection()

print_header(
    "AVG() OVER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each row, compute the average UnitPrice globally and per Country.
#
# Key idea: AVG() OVER (PARTITION BY Country) for the country-level average;
#           AVG() OVER () with no partition for the global average.

user_sql_1 = """
    SELECT
        Country,
        StockCode,
        UnitPrice,
        AVG(UnitPrice) OVER (PARTITION BY Country) AS country_avg_price,
        AVG(UnitPrice) OVER ()                     AS global_avg_price
    FROM retail_data
    WHERE UnitPrice > 0
"""




check_exercise(
    number=1,
    description="Average unit price per country and global average on every row",
    user_sql=user_sql_1,
    validation_fn=validate_avg_ex1,
    con=con,
    hint="AVG(UnitPrice) OVER (PARTITION BY Country) and AVG(UnitPrice) OVER () for the global average",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Compute the running average invoice revenue per customer and flag each row
# as 'above_avg' or 'below_avg'.
#
# Key idea: aggregate invoice revenue in a CTE first, then
#           AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
#           gives a running (i.e., cumulative) average up to the current row.

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
        AVG(invoice_revenue) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
        ) AS running_avg,
        CASE
            WHEN invoice_revenue > AVG(invoice_revenue) OVER (
                PARTITION BY CustomerID ORDER BY InvoiceDate
            ) THEN 'above_avg'
            ELSE 'below_avg'
        END AS spend_trend
    FROM invoice_revenue
"""




check_exercise(
    number=2,
    description="Running average invoice spend per customer with above/below flag",
    user_sql=user_sql_2,
    validation_fn=validate_avg_ex2,
    con=con,
    hint="CTE for invoice revenue; AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate); CASE WHEN invoice_revenue > running_avg THEN 'above_avg' ELSE 'below_avg' END",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# 3-invoice moving average vs all-time average per customer.
#
# Key idea:
#   - avg_all_time: AVG() OVER (PARTITION BY CustomerID) — no ORDER BY, full partition.
#   - moving_avg_3: AVG() OVER (... ORDER BY InvoiceDate ROWS BETWEEN 2 PRECEDING AND CURRENT ROW).

user_sql_3 = """
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
        AVG(invoice_revenue) OVER (PARTITION BY CustomerID) AS avg_all_time,
        AVG(invoice_revenue) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) AS moving_avg_3
    FROM invoice_revenue
"""




check_exercise(
    number=3,
    description="3-invoice moving average vs all-time average per customer",
    user_sql=user_sql_3,
    validation_fn=validate_avg_ex3,
    con=con,
    hint="AVG(invoice_revenue) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3",
)
