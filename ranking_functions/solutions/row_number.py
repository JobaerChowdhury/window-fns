"""
solutions/row_number.py — ROW_NUMBER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the ROW_NUMBER() exercises.
Refer to this file ONLY if you are stuck on exercises/row_number.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_row_number_ex1, validate_row_number_ex2, validate_row_number_ex3

con = get_connection()

print_header(
    "ROW_NUMBER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Assign a row number to each invoice line within each Country,
# ordered by Quantity DESC. Row 1 should be the highest-quantity line per country.
#
# Key idea: PARTITION BY Country so each country gets its own row numbering;
#           ORDER BY Quantity DESC so the highest-quantity line is row 1.

user_sql_1 = """
    SELECT
        Country,
        InvoiceNo,
        Description,
        Quantity,
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Quantity DESC) AS row_num
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
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# Find each customer's SECOND purchase.
#
# Key idea: use a CTE to number all purchases per customer ordered by date,
#           then filter the outer query WHERE purchase_num = 2.

user_sql_2 = """
    WITH numbered_purchases AS (
        SELECT
            CustomerID,
            InvoiceDate,
            InvoiceNo,
            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS purchase_num
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
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# De-duplicate: keep only one row per (InvoiceNo, StockCode) combination.
#
# Key idea: PARTITION BY InvoiceNo, StockCode gives every duplicate group its
#           own numbering; keeping row_num = 1 eliminates all duplicates.

user_sql_3 = """
    WITH numbered_data AS (
        SELECT
            InvoiceNo,
            StockCode,
            CustomerID,
            InvoiceDate,
            ROW_NUMBER() OVER (PARTITION BY InvoiceNo, StockCode ORDER BY InvoiceDate) AS row_num
        FROM retail_data
        WHERE InvoiceNo IS NOT NULL AND StockCode IS NOT NULL
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
