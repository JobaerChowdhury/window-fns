"""
exercises/first_value.py — FIRST_VALUE() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/first_value.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/first_value.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_first_value_ex1, validate_first_value_ex2, validate_first_value_ex3

con = get_connection()

print_header(
    "FIRST_VALUE() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# For each invoice line, show the StockCode of the FIRST item the customer
# ever purchased (by InvoiceDate). Every row for a customer should carry
# the same first_stockcode value.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, StockCode,
#                   first_stockcode

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: FIRST_VALUE(StockCode) OVER (
    --           PARTITION BY CustomerID
    --           ORDER BY InvoiceDate
    --           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    --       ) AS first_stockcode
"""


user_sql_1 = """
    SELECT 
        CustomerID, 
        InvoiceDate, 
        InvoiceNo, 
        StockCode, 
        FIRST_VALUE(StockCode) OVER(
            PARTITION BY CustomerID 
            ORDER BY InvoiceDate 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as first_stockcode
    FROM retail_data 
"""



check_exercise(
    number=1,
    description="Show the first-ever StockCode purchased by each customer on every row",
    user_sql=user_sql_1,
    validation_fn=validate_first_value_ex1,
    con=con,
    hint="FIRST_VALUE(StockCode) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# For each StockCode in each Country, compute avg_price and attach the
# price of the CHEAPEST StockCode in that Country (cheapest_in_country).
# Order by avg_price ASC within the partition so FIRST_VALUE picks the minimum.
# Use a frame clause to ensure correctness.
#
# Required columns: Country, StockCode, avg_price, cheapest_in_country

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: aggregate AVG(UnitPrice) per (Country, StockCode) first,
    --       then FIRST_VALUE(avg_price) OVER (PARTITION BY Country ORDER BY avg_price ASC
    --           ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS cheapest_in_country
"""



user_sql_2 = """
    WITH avg_price AS (
        SELECT 
            Country, 
            StockCode, 
            ROUND(AVG(UnitPrice), 2) AS avg_price
        FROM retail_data 
        WHERE UnitPrice > 0 
        GROUP BY Country, StockCode
    )
    SELECT 
        Country, 
        StockCode, 
        avg_price, 
        FIRST_VALUE(avg_price) OVER( 
            PARTITION BY Country
            ORDER BY avg_price ASC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as cheapest_in_country
    FROM avg_price 
"""



check_exercise(
    number=2,
    description="Attach each country's cheapest avg product price to every row",
    user_sql=user_sql_2,
    validation_fn=validate_first_value_ex2,
    con=con,
    hint="Aggregate AVG(UnitPrice) first, then FIRST_VALUE(avg_price) OVER (PARTITION BY Country ORDER BY avg_price ASC ROWS UNBOUNDED ...)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# Find the time elapsed (in days) from each customer's very first purchase
# to every subsequent purchase. Every row should carry the same
# first_purchase_day. Rows on the first purchase day should have
# days_since_first = 0.
#
# Required columns: CustomerID, invoice_day, InvoiceNo,
#                   first_purchase_day, days_since_first

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: cast InvoiceDate with STRPTIME, then
    --   FIRST_VALUE(invoice_day) OVER (PARTITION BY CustomerID ORDER BY invoice_day
    --       ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS first_purchase_day
    -- then DATEDIFF('day', first_purchase_day, invoice_day) AS days_since_first
"""


user_sql_3 = """
    WITH dated_purchase AS (
        SELECT 
            CustomerID, 
            InvoiceNo, 
            CAST(STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS DATE) AS invoice_day
        FROM retail_data 
        WHERE CustomerID IS NOT NULL 
    )
    SELECT 
        CustomerID, 
        InvoiceNo, 
        invoice_day,        
        FIRST_VALUE(invoice_day) OVER(
            PARTITION BY CustomerID 
            ORDER BY invoice_day 
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_purchase_day,
        DATEDIFF(
            'day', 
            FIRST_VALUE(invoice_day) OVER(
                PARTITION BY CustomerID 
                ORDER BY invoice_day 
                ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
            ),             
            invoice_day
        ) AS days_since_first

    FROM dated_purchase 
"""



check_exercise(
    number=3,
    description="Days elapsed since each customer's first-ever purchase",
    user_sql=user_sql_3,
    validation_fn=validate_first_value_ex3,
    con=con,
    hint="FIRST_VALUE(invoice_day) OVER (...) AS first_purchase_day, then DATEDIFF('day', first_purchase_day, invoice_day)",
)
