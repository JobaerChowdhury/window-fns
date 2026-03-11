"""
exercises/08_rank_within_category.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex8

con = get_connection()

print_header(
    "Interview Question 8",
    "Rank customers based on their total spend within their respective countries.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 8
# ════════════════════════════════════════════════════════════════════════════

user_sql_8 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=8,
    description="Rank customers based on their total spend within their respective countries.",
    user_sql=user_sql_8,
    validation_fn=validate_ex8,
    con=con,
    hint_key=8,
)
