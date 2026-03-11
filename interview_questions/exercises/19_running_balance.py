"""
exercises/19_running_balance.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex19

con = get_connection()

print_header(
    "Interview Question 19",
    "Calculate the running total of units sold for StockCode '22423' over time.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 19
# ════════════════════════════════════════════════════════════════════════════

user_sql_19 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=19,
    description="Calculate the running total of units sold for StockCode '22423' over time.",
    user_sql=user_sql_19,
    validation_fn=validate_ex19,
    con=con,
    hint_key=19,
)
