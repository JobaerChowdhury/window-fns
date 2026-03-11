"""
exercises/lead.py — LEAD() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/lead.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/lead.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_lead_ex1, validate_lead_ex2, validate_lead_ex3

con = get_connection()

print_header(
    "LEAD() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each distinct customer invoice, show the InvoiceNo of the NEXT invoice
# for the same customer (ordered by InvoiceDate). The last invoice per
# customer should return NULL for next_invoice_no.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, next_invoice_no

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: LEAD(InvoiceNo, 1) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
    -- Use SELECT DISTINCT or group to one row per invoice first.
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
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Compute the number of days until each customer's next purchase.
# Work at the invoice level (DISTINCT CustomerID, InvoiceDate, InvoiceNo).
# Cast InvoiceDate to DATE before computing the gap.
# The last invoice per customer should have NULL days_until_next.
#
# Required columns: CustomerID, invoice_day, InvoiceNo, next_invoice_day,
#                   days_until_next

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: CTE with CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE)
    --       then LEAD(invoice_day) and DATEDIFF('day', invoice_day, next_invoice_day)
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
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# Find each customer's penultimate (second-to-last) invoice.
# Strategy: use LEAD(InvoiceDate, 1) — when the next-next (LEAD offset 2)
# is NULL, the current row is the second-to-last. Return only those rows.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: CTE with DISTINCT invoices; add LEAD(..., 1) and LEAD(..., 2).
    --       Filter WHERE the LEAD-2 value IS NULL AND LEAD-1 IS NOT NULL.
"""


check_exercise(
    number=3,
    description="Find each customer's penultimate (second-to-last) invoice",
    user_sql=user_sql_3,
    validation_fn=validate_lead_ex3,
    con=con,
    hint="LEAD(InvoiceDate, 2) IS NULL AND LEAD(InvoiceDate, 1) IS NOT NULL identifies the second-to-last row",
)
