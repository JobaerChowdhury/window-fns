"""
exercises/04_moving_average.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex4

con = get_connection()

print_header(
    "Interview Question 4",
    "Calculate a 3-invoice rolling average of the invoice total (Quantity * UnitPrice) for CustomerID 17850.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 4
# ════════════════════════════════════════════════════════════════════════════

user_sql_4 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=4,
    description="Calculate a 3-invoice rolling average of the invoice total (Quantity * UnitPrice) for CustomerID 17850.",
    user_sql=user_sql_4,
    validation_fn=validate_ex4,
    con=con,
    hint_key=4,
)
