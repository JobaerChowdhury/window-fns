"""
exercises/10_gap_detection.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex10

con = get_connection()

print_header(
    "Interview Question 10",
    "Find the largest gap in days between consecutive purchases for CustomerID 17850.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 10
# ════════════════════════════════════════════════════════════════════════════

user_sql_10 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=10,
    description="Find the largest gap in days between consecutive purchases for CustomerID 17850.",
    user_sql=user_sql_10,
    validation_fn=validate_ex10,
    con=con,
    hint_key=10,
)
