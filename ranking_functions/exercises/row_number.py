"""
exercises/row_number.py — ROW_NUMBER() Exercises
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complete the three exercises below. For each one:
  1. Replace the placeholder comment with your SQL
  2. Run:  python exercises/row_number.py
  3. Check the ✅ PASS / ❌ FAIL output

Not sure where to start? First run: python tutorials/row_number.py
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_row_number_ex1, validate_row_number_ex2, validate_row_number_ex3

con = get_connection()

print_header(
    "ROW_NUMBER() — Exercises",
    "Write SQL for each exercise below. Re-run this file after each attempt.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════
# Assign a row number to each invoice line within each Country,
# ordered by Quantity DESC. Row 1 should be the highest-quantity line per country.
#
# Required columns: Country, InvoiceNo, Description, Quantity, row_num

user_sql_1 = """
    -- YOUR SQL HERE
    -- Hint: ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Quantity DESC)
    -- Make sure to include: Country, InvoiceNo, Description, Quantity, row_num
"""

user_sql_1 = """ 
    SELECT
        Country, 
        InvoiceNo, 
        Description, 
        Quantity, 
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Quantity DESC) as row_num
    FROM retail_data
"""


check_exercise(
    number=1,
    description="Number invoice lines by Quantity DESC within each Country",
    user_sql=user_sql_1,
    validation_fn=validate_row_number_ex1,
    con=con,
    hint="ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Quantity DESC)",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════
# Find each customer's SECOND purchase.
# Expected: one row per customer, where purchase_num = 2.
#
# Required columns: CustomerID, InvoiceDate, InvoiceNo, purchase_num

user_sql_2 = """
    -- YOUR SQL HERE
    -- Hint: wrap a ROW_NUMBER() window in a CTE, then filter WHERE purchase_num = 2
    -- Expected columns: CustomerID, InvoiceDate, InvoiceNo, purchase_num
"""


user_sql_2 = """
    WITH numbered_purchases AS (
        SELECT 
            CustomerID, 
            InvoiceDate, 
            InvoiceNo, 
            ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) as purchase_num
        FROM retail_data
        WHERE CustomerID IS NOT NULL
    )
    SELECT 
        CustomerID, InvoiceDate, InvoiceNo, purchase_num
    FROM numbered_purchases
    WHERE purchase_num = 2
"""



check_exercise(
    number=2,
    description="Find each customer's second purchase",
    user_sql=user_sql_2,
    validation_fn=validate_row_number_ex2,
    con=con,
    hint="Use a CTE with ROW_NUMBER(), then filter WHERE purchase_num = 2",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════
# De-duplicate: keep only one row per (InvoiceNo, StockCode) combination.
# Use ROW_NUMBER() partitioned by InvoiceNo and StockCode, then filter on rn = 1.
# Expected: no duplicate (InvoiceNo, StockCode) pairs in result.

user_sql_3 = """
    -- YOUR SQL HERE
    -- Hint: PARTITION BY InvoiceNo, StockCode — ORDER BY any column to break ties
    -- Filter WHERE rn = 1
"""


user_sql_3 = """
    WITH numbered_data AS (
        SELECT 
            InvoiceNo,
            StockCode,
            CustomerID, 
            InvoiceDate,              
            ROW_NUMBER() OVER(PARTITION BY InvoiceNo, StockCode ORDER BY InvoiceDate) as row_num
        FROM retail_data
        WHERE (InvoiceNo IS NOT NULL AND StockCode IS NOT NULL)
    ) 
    SELECT   
        InvoiceNo, StockCode, CustomerID, InvoiceDate
    FROM numbered_data
    WHERE row_num = 1
"""



check_exercise(
    number=3,
    description="De-duplicate rows by (InvoiceNo, StockCode) using ROW_NUMBER()",
    user_sql=user_sql_3,
    validation_fn=validate_row_number_ex3,
    con=con,
    hint="PARTITION BY InvoiceNo, StockCode then filter WHERE rn = 1",
)
