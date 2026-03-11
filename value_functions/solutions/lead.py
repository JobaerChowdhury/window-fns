"""
solutions/lead.py — LEAD() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the LEAD() exercises.
Refer to this file ONLY if you are stuck on exercises/lead.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_lead_ex1, validate_lead_ex2, validate_lead_ex3

con = get_connection()

print_header(
    "LEAD() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each distinct customer invoice, show the InvoiceNo of the NEXT invoice
# for the same customer.
#
# Key idea: LEAD(InvoiceNo, 1) looks forward 1 row. The last invoice per
#           customer has no successor → NULL.

user_sql_1 = """
    WITH distinct_invoices AS (
        SELECT DISTINCT
            CustomerID,
            InvoiceDate,
            InvoiceNo
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        LEAD(InvoiceNo, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS next_invoice_no
    FROM distinct_invoices
"""


check_exercise(
    number=1,
    description="Show each customer's next invoice number",
    user_sql=user_sql_1,
    validation_fn=validate_lead_ex1,
    con=con,
    hint="LEAD(InvoiceNo, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS next_invoice_no",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Compute the number of days until each customer's next purchase.
#
# Key idea: parse InvoiceDate to a DATE first (STRPTIME → CAST AS DATE),
#           then LEAD(invoice_day) to get next_invoice_day,
#           then DATEDIFF('day', invoice_day, next_invoice_day).

user_sql_2 = """
    WITH distinct_invoices AS (
        SELECT DISTINCT
            CustomerID,
            CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE) AS invoice_day,
            InvoiceNo
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    )
    SELECT
        CustomerID,
        invoice_day,
        InvoiceNo,
        LEAD(invoice_day) OVER (PARTITION BY CustomerID ORDER BY invoice_day) AS next_invoice_day,
        DATEDIFF(
            'day',
            invoice_day,
            LEAD(invoice_day) OVER (PARTITION BY CustomerID ORDER BY invoice_day)
        ) AS days_until_next
    FROM distinct_invoices
"""


check_exercise(
    number=2,
    description="Days until each customer's next purchase",
    user_sql=user_sql_2,
    validation_fn=validate_lead_ex2,
    con=con,
    hint="LEAD(invoice_day) OVER ... then DATEDIFF('day', invoice_day, next_invoice_day)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Find each customer's penultimate (second-to-last) invoice.
#
# Key idea: use LEAD(..., 1) and LEAD(..., 2) in a CTE.
#           The penultimate row has LEAD-1 IS NOT NULL (there is a next row)
#           AND LEAD-2 IS NULL (there is no row after that).

user_sql_3 = """
    WITH distinct_invoices AS (
        SELECT DISTINCT
            CustomerID,
            InvoiceDate,
            InvoiceNo
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    ), with_lead AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            LEAD(InvoiceDate, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS next1,
            LEAD(InvoiceDate, 2) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS next2
        FROM distinct_invoices
    )
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo
    FROM with_lead
    WHERE next1 IS NOT NULL AND next2 IS NULL
"""


check_exercise(
    number=3,
    description="Find each customer's penultimate (second-to-last) invoice",
    user_sql=user_sql_3,
    validation_fn=validate_lead_ex3,
    con=con,
    hint="LEAD(InvoiceDate, 2) IS NULL AND LEAD(InvoiceDate, 1) IS NOT NULL identifies the second-to-last row",
)
