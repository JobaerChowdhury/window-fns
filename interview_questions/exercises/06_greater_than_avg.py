"""
exercises/06_greater_than_avg.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex6

con = get_connection()

print_header(
    "Interview Question 6",
    "Identify invoices where the total invoice amount is greater than the average invoice amount for that invoice's Country.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 6
# ════════════════════════════════════════════════════════════════════════════

user_sql_6 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=6,
    description="Identify invoices where the total invoice amount is greater than the average invoice amount for that invoice's Country.",
    user_sql=user_sql_6,
    validation_fn=validate_ex6,
    con=con,
    hint_key=6,
)
