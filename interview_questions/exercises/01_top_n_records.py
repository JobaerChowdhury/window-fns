"""
exercises/01_top_n_records.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex1

con = get_connection()

print_header(
    "Interview Question 1",
    "Find the top 3 most expensive products (UnitPrice) per Country.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 1
# ════════════════════════════════════════════════════════════════════════════

user_sql_1 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=1,
    description="Find the top 3 most expensive products (UnitPrice) per Country.",
    user_sql=user_sql_1,
    validation_fn=validate_ex1,
    con=con,
    hint_key=1,
)
