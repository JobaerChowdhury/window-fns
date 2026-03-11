"""
exercises/05_consecutive_purchases.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex5

con = get_connection()

print_header(
    "Interview Question 5",
    "Find customers who made purchases on 3 consecutive days.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 5
# ════════════════════════════════════════════════════════════════════════════

user_sql_5 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=5,
    description="Find customers who made purchases on 3 consecutive days.",
    user_sql=user_sql_5,
    validation_fn=validate_ex5,
    con=con,
    hint_key=5,
)
