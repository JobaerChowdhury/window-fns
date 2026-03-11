"""
exercises/18_increasing_trend.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex18

con = get_connection()

print_header(
    "Interview Question 18",
    "Identify products whose monthly sales quantity increased compared to the previous month.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 18
# ════════════════════════════════════════════════════════════════════════════

user_sql_18 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=18,
    description="Identify products whose monthly sales quantity increased compared to the previous month.",
    user_sql=user_sql_18,
    validation_fn=validate_ex18,
    con=con,
    hint_key=18,
)
