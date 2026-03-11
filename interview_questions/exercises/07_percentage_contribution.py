"""
exercises/07_percentage_contribution.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex7

con = get_connection()

print_header(
    "Interview Question 7",
    "Calculate each country's percentage contribution to the total global revenue.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 7
# ════════════════════════════════════════════════════════════════════════════

user_sql_7 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=7,
    description="Calculate each country's percentage contribution to the total global revenue.",
    user_sql=user_sql_7,
    validation_fn=validate_ex7,
    con=con,
    hint_key=7,
)
