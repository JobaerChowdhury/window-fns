"""
exercises/17_bucket_data.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex17

con = get_connection()

print_header(
    "Interview Question 17",
    "Divide customers into 4 spending tiers (quartiles) based on their total spend.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 17
# ════════════════════════════════════════════════════════════════════════════

user_sql_17 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=17,
    description="Divide customers into 4 spending tiers (quartiles) based on their total spend.",
    user_sql=user_sql_17,
    validation_fn=validate_ex17,
    con=con,
    hint_key=17,
)
