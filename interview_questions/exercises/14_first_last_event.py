"""
exercises/14_first_last_event.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex14

con = get_connection()

print_header(
    "Interview Question 14",
    "Return the first and last product (StockCode) purchased by each customer based on InvoiceDate.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 14
# ════════════════════════════════════════════════════════════════════════════

user_sql_14 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=14,
    description="Return the first and last product (StockCode) purchased by each customer based on InvoiceDate.",
    user_sql=user_sql_14,
    validation_fn=validate_ex14,
    con=con,
    hint_key=14,
)
