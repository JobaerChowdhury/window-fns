"""
exercises/20_detect_status_changes.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex20

con = get_connection()

print_header(
    "Interview Question 20",
    "Detect when a customer changes their shipping Country over time.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 20
# ════════════════════════════════════════════════════════════════════════════

user_sql_20 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=20,
    description="Detect when a customer changes their shipping Country over time.",
    user_sql=user_sql_20,
    validation_fn=validate_ex20,
    con=con,
    hint_key=20,
)
