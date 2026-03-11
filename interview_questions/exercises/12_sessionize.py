"""
exercises/12_sessionize.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex12

con = get_connection()

print_header(
    "Interview Question 12",
    "Group invoices for CustomerID 17850 into sessions. Consider a gap of >60 minutes as a new session.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 12
# ════════════════════════════════════════════════════════════════════════════

user_sql_12 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=12,
    description="Group invoices for CustomerID 17850 into sessions. Consider a gap of >60 minutes as a new session.",
    user_sql=user_sql_12,
    validation_fn=validate_ex12,
    con=con,
    hint_key=12,
)
