"""
exercises/03_running_total.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex3

con = get_connection()

print_header(
    "Interview Question 3",
    "Calculate the cumulative quantity of StockCode '85123A' sold over time, ordered by InvoiceDate.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 3
# ════════════════════════════════════════════════════════════════════════════

user_sql_3 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=3,
    description="Calculate the cumulative quantity of StockCode '85123A' sold over time, ordered by InvoiceDate.",
    user_sql=user_sql_3,
    validation_fn=validate_ex3,
    con=con,
    hint_key=3,
)
