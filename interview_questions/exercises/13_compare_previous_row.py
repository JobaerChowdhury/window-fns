"""
exercises/13_compare_previous_row.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex13

con = get_connection()

print_header(
    "Interview Question 13",
    "Calculate the week-over-week revenue growth for the entire dataset.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 13
# ════════════════════════════════════════════════════════════════════════════

user_sql_13 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=13,
    description="Calculate the week-over-week revenue growth for the entire dataset.",
    user_sql=user_sql_13,
    validation_fn=validate_ex13,
    con=con,
    hint_key=13,
)
