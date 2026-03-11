"""
solutions/count.py — COUNT() OVER() Exercise Solutions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reference solutions for the COUNT() OVER() exercises.
Refer to this file ONLY if you are stuck on exercises/count.py.

Running this file will verify all three solutions pass.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_count_ex1, validate_count_ex2, validate_count_ex3

con = get_connection()

print_header(
    "COUNT() OVER() — Solutions",
    "Reference solutions — run to confirm all exercises pass.",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 1 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For every row, attach the total number of rows in that country
# (country_row_count) and the total number of rows in the whole dataset
# (global_row_count).
#
# Key idea: COUNT(*) OVER (PARTITION BY Country) → per-country row count;
#           COUNT(*) OVER ()                     → total dataset row count.

user_sql_1 = """
    SELECT
        Country,
        InvoiceNo,
        StockCode,
        COUNT(*) OVER (PARTITION BY Country) AS country_row_count,
        COUNT(*) OVER ()                     AS global_row_count
    FROM retail_data
"""




check_exercise(
    number=1,
    description="Row count per country and total row count on every row",
    user_sql=user_sql_1,
    validation_fn=validate_count_ex1,
    con=con,
    hint="COUNT(*) OVER (PARTITION BY Country) and COUNT(*) OVER () for the global count",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 2 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For each customer, compute a running count of invoice line-item rows
# ordered by InvoiceDate.
#
# Key idea: COUNT(*) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)
#           uses the default running-frame (ROWS UNBOUNDED PRECEDING TO CURRENT ROW),
#           so it increments by 1 for each new row processed in order.

user_sql_2 = """
    SELECT
        CustomerID,
        InvoiceDate,
        InvoiceNo,
        StockCode,
        COUNT(*) OVER (
            PARTITION BY CustomerID
            ORDER BY InvoiceDate
        ) AS row_seq
    FROM retail_data
    WHERE CustomerID IS NOT NULL
"""




check_exercise(
    number=2,
    description="Running row counter per customer ordered by InvoiceDate",
    user_sql=user_sql_2,
    validation_fn=validate_count_ex2,
    con=con,
    hint="COUNT(*) OVER (PARTITION BY CustomerID ORDER BY InvoiceDate) AS row_seq",
)


# ════════════════════════════════════════════════════════════════════════════
# Exercise 3 — Solution
# ════════════════════════════════════════════════════════════════════════════
# For every row, compute the % of rows in the same Country with a non-NULL
# CustomerID (pct_identified).
#
# Key idea: COUNT(CustomerID) counts only non-NULL values (SQL standard),
#           while COUNT(*) counts all rows including NULLs.
#           Dividing them gives the identified fraction per country.

user_sql_3 = """
    SELECT
        Country,
        InvoiceNo,
        CustomerID,
        COUNT(CustomerID) OVER (PARTITION BY Country) AS identified_rows,
        COUNT(*)          OVER (PARTITION BY Country) AS total_rows,
        ROUND(
            100.0 * COUNT(CustomerID) OVER (PARTITION BY Country)
                  / COUNT(*)          OVER (PARTITION BY Country),
            1
        ) AS pct_identified
    FROM retail_data
"""




check_exercise(
    number=3,
    description="Identified customer percentage per country on every row",
    user_sql=user_sql_3,
    validation_fn=validate_count_ex3,
    con=con,
    hint="COUNT(CustomerID) OVER (PARTITION BY Country) for non-NULLs; COUNT(*) OVER (PARTITION BY Country) for total; divide and multiply by 100",
)
