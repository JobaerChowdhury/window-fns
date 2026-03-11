"""
exercises/02_second_purchase.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex2

con = get_connection()

print_header(
    "Interview Question 2",
    "Find the second purchase (InvoiceNo and InvoiceDate) made by each CustomerID.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 2
# ════════════════════════════════════════════════════════════════════════════

user_sql_2 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=2,
    description="Find the second purchase (InvoiceNo and InvoiceDate) made by each CustomerID.",
    user_sql=user_sql_2,
    validation_fn=validate_ex2,
    con=con,
    hint_key=2,
)
