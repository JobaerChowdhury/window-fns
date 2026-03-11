# 20 Advanced SQL Window Function Interview Questions 
*(Adapted for the Online Retail Dataset)*

*Assume the table is named `retail` with columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate` (String: 'M/D/YYYY H:MM'), `UnitPrice`, `CustomerID`, `Country`.*

## 1. Top N Records Per Group
**Problem:** Find the top 3 most expensive products (`UnitPrice`) per `Country`.
*(Hint: Use `ROW_NUMBER()` or `RANK()`. Since `StockCode` could appear multiple times, make sure you look at distinct products.)*

## 2. Second Purchase per Customer
**Problem:** Find the second purchase (`InvoiceNo` and `InvoiceDate`) made by each `CustomerID`.
*(Hint: Order by parsed `InvoiceDate` and use `ROW_NUMBER()`.)*

## 3. Running Total of Sales
**Problem:** Calculate the cumulative quantity of StockCode `'85123A'` sold over time, ordered by `InvoiceDate`.

## 4. Moving Average (3-Day Rolling Average)
**Problem:** Calculate a 3-invoice rolling average of the invoice total (`Quantity * UnitPrice`) for CustomerID `17850`.
*(Hint: Group by `InvoiceNo` and `InvoiceDate` first, then calculate the moving average.)*

## 5. Detect Consecutive Logins (Consecutive Purchases)
**Problem:** Find customers who made purchases on 3 consecutive days.
*(Hint: Cast `InvoiceDate` to `DATE`. Use `LAG()` with an offset of 2 to find a 2-day gap between the current and previous 2nd row.)*

## 6. Identify Salary Greater Than Department Average
**Problem:** Identify invoices (`InvoiceNo`) where the total invoice amount is greater than the average invoice amount for that invoice's `Country`.

## 7. Percentage Contribution of Each Product
**Problem:** Calculate each country's percentage contribution to the total global revenue.

## 8. Rank Products by Revenue Within Category
**Problem:** Rank customers based on their total spend within their respective countries.

## 9. Find Duplicate Records
**Problem:** Find duplicate line items (same `InvoiceNo` and `StockCode` combination) ordered by `Quantity` descending.

## 10. Gap Detection in IDs (Time Gaps)
**Problem:** Find the largest gap in days between consecutive purchases for CustomerID `17850`.

## 11. Find Longest Streak of Activity
**Problem:** Find the longest streak of consecutive daily purchases for each customer.
*(Hint: Use the gap-and-island technique by subtracting a `ROW_NUMBER()` from the purchase date.)*

## 12. Sessionize User Activity
**Problem:** Group invoices for CustomerID `17850` into sessions. Consider a gap of more than 60 minutes between purchases as the start of a new session. Calculate the `session_id`.

## 13. Compare Current Row with Previous Row
**Problem:** Calculate the week-over-week revenue growth for the entire dataset.
*(Hint: Truncate dates to the start of the week and use `LAG()` to compare weekly revenue.)*

## 14. Identify First and Last Event Per User
**Problem:** Return the first and last product (`StockCode`) purchased by each customer based on `InvoiceDate`.

## 15. Top Performing Day per Store
**Problem:** Find the highest revenue day for each `Country`.

## 16. Percentile Ranking
**Problem:** Calculate the percentile rank of each customer's total spend.

## 17. Bucket Data into Groups
**Problem:** Divide customers into 4 spending tiers (quartiles) based on their total spend.

## 18. Find Products with Increasing Sales Trend
**Problem:** Identify products (`StockCode`) whose monthly sales quantity increased compared to the previous month.

## 19. Running Balance Calculation
**Problem:** Calculate the running total of units sold for StockCode `'22423'` over time.

## 20. Detect Changes in Status
**Problem:** Detect when a customer changes their shipping `Country` over time (i.e. lists a different `Country` than their previous invoice).
