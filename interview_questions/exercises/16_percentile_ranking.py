"""
exercises/16_percentile_ranking.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex16

con = get_connection()

print_header(
    "Interview Question 16",
    "Calculate the percentile rank of each customer's total spend.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 16
# ════════════════════════════════════════════════════════════════════════════

user_sql_16 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=16,
    description="Calculate the percentile rank of each customer's total spend.",
    user_sql=user_sql_16,
    validation_fn=validate_ex16,
    con=con,
    hint_key=16,
)
