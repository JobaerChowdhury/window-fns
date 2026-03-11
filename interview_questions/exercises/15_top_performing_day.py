"""
exercises/15_top_performing_day.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex15

con = get_connection()

print_header(
    "Interview Question 15",
    "Find the highest revenue day for each Country.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 15
# ════════════════════════════════════════════════════════════════════════════

user_sql_15 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=15,
    description="Find the highest revenue day for each Country.",
    user_sql=user_sql_15,
    validation_fn=validate_ex15,
    con=con,
    hint_key=15,
)
