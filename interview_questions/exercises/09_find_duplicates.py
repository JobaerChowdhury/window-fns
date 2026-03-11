"""
exercises/09_find_duplicates.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from setup import get_connection, check_exercise, print_header
from validators import validate_ex9

con = get_connection()

print_header(
    "Interview Question 9",
    "Find duplicate line items (same InvoiceNo and StockCode combination) ordered by Quantity descending.",
)

# ════════════════════════════════════════════════════════════════════════════
# Exercise 9
# ════════════════════════════════════════════════════════════════════════════

user_sql_9 = """
    -- YOUR SQL HERE
"""

check_exercise(
    number=9,
    description="Find duplicate line items (same InvoiceNo and StockCode combination) ordered by Quantity descending.",
    user_sql=user_sql_9,
    validation_fn=validate_ex9,
    con=con,
    hint_key=9,
)
