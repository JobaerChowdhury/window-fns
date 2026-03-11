"""
hints.py \u2014 Hints for the 20 advanced SQL interview questions.
"""

HINTS = {
    1: "Use ROW_NUMBER() or RANK() OVER (PARTITION BY Country ORDER BY UnitPrice DESC)",
    2: "Order by parsed InvoiceDate: strptime(InvoiceDate, '%m/%d/%Y %-H:%M') and use ROW_NUMBER()",
    3: "Use SUM(Quantity) OVER(ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
    4: "Group by InvoiceNo/Date first to get totals, then AVG() OVER with ROWS BETWEEN 2 PRECEDING AND CURRENT ROW",
    5: "Cast InvoiceDate to DATE, then use LAG(..., 2) to find a difference of exactly 2 days",
    6: "Calculate invoice totals in a CTE, then AVG() OVER(PARTITION BY Country) to compare",
    7: "Revenue * 100.0 / SUM(Revenue) OVER()",
    8: "Aggregate total spend per customer and country, then RANK() OVER(PARTITION BY Country ORDER BY TotalSpend DESC)",
    9: "Use ROW_NUMBER() OVER(PARTITION BY InvoiceNo, StockCode ORDER BY Quantity DESC), then filter for rn > 1",
    10: "Use LAG() OVER(ORDER BY PurchaseDate) to track the gap between rows",
    11: "Gap-and-island: subtract ROW_NUMBER() from the date to identify consecutive streaks",
    12: "Use LAG() to find time diff. Use a CASE statement to flag new sessions (1 or 0), then SUM() OVER to create session IDs",
    13: "Truncate date to week, then use LAG(Revenue) to compare with current Week's revenue",
    14: "Use FIRST_VALUE() and LAST_VALUE() with proper ROWS BETWEEN boundaries",
    15: "Calculate daily revenue per country, then use ROW_NUMBER() OVER(PARTITION BY Country ORDER BY Revenue DESC)",
    16: "Group by CustomerID to get total spend, then use PERCENT_RANK() OVER(ORDER BY TotalSpend)",
    17: "Group by CustomerID for total spend, then use NTILE(4) OVER(ORDER BY TotalSpend DESC)",
    18: "Use date_trunc('month', ...) to aggregate monthly sales, then LAG() to compare to previous month's total",
    19: "Use SUM(Quantity) OVER(ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M') ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)",
    20: "Use LAG(Country) OVER(PARTITION BY CustomerID ORDER BY EventTime) and isolate where the country changes"
}
