"""
exercises/11_longest_streak.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex11

con = get_connection()

print_header(
    "Interview Question 11",
    "Find the longest streak of consecutive daily purchases for each customer.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 11
# ════════════════════════════════════════════════════════════════════════════

user_sql_11 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=11,
    description="Find the longest streak of consecutive daily purchases for each customer.",
    user_sql=user_sql_11,
    validation_fn=validate_ex11,
    con=con,
    hint_key=11,
)
