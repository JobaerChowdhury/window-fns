# 20 Advanced SQL Window Function Interview Solutions
*(Adapted for the Online Retail Dataset)*

*Assume the table is named `retail_data`.*

## 1. Top N Records Per Group
```sql
SELECT * FROM (
    SELECT DISTINCT StockCode, Description, Country, UnitPrice,
           ROW_NUMBER() OVER(PARTITION BY Country ORDER BY UnitPrice DESC) as rn
    FROM retail_data
) WHERE rn <= 3;
```

## 2. Second Purchase per Customer
```sql
SELECT CustomerID, InvoiceNo, InvoiceDate
FROM (
    SELECT CustomerID, InvoiceNo, InvoiceDate,
           ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M')) as rn
    FROM (SELECT DISTINCT CustomerID, InvoiceNo, InvoiceDate FROM retail_data WHERE CustomerID IS NOT NULL)
) WHERE rn = 2;
```

## 3. Running Total of Sales
```sql
SELECT InvoiceDate, Quantity,
       SUM(Quantity) OVER(ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M') ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as running_qty
FROM retail_data
WHERE StockCode = '85123A';
```

## 4. Moving Average (3-Day Rolling Average)
```sql
WITH InvoiceTotals AS (
    SELECT CustomerID, InvoiceNo, InvoiceDate, SUM(Quantity * UnitPrice) as InvoiceTotal
    FROM retail_data
    WHERE CustomerID = 17850
    GROUP BY CustomerID, InvoiceNo, InvoiceDate
)
SELECT InvoiceNo, InvoiceDate, InvoiceTotal,
       AVG(InvoiceTotal) OVER (ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M') ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg
FROM InvoiceTotals;
```

## 5. Detect Consecutive Logins (Data: Consecutive Purchases)
```sql
WITH DailyPurchases AS (
    SELECT DISTINCT CustomerID, CAST(strptime(InvoiceDate, '%m/%d/%Y %-H:%M') AS DATE) as PurchaseDate
    FROM retail_data
    WHERE CustomerID IS NOT NULL
),
DateDiffs AS (
    SELECT CustomerID, PurchaseDate,
           PurchaseDate - CAST(LAG(PurchaseDate, 2) OVER(PARTITION BY CustomerID ORDER BY PurchaseDate) as DATE) as diff_days
    FROM DailyPurchases
)
SELECT DISTINCT CustomerID FROM DateDiffs WHERE CAST(diff_days AS INTEGER) = 2;
```

## 6. Identify Salary Greater Than Department Average (Data: Invoice Greater Than Country Average)
```sql
WITH InvoiceTotals AS (
    SELECT InvoiceNo, Country, SUM(Quantity * UnitPrice) as InvoiceTotal
    FROM retail_data
    GROUP BY InvoiceNo, Country
),
CountryAvgs AS (
    SELECT InvoiceNo, Country, InvoiceTotal,
           AVG(InvoiceTotal) OVER(PARTITION BY Country) as CountryAvg
    FROM InvoiceTotals
)
SELECT InvoiceNo, Country, InvoiceTotal, CountryAvg
FROM CountryAvgs
WHERE InvoiceTotal > CountryAvg;
```

## 7. Percentage Contribution of Each Product
```sql
WITH CountryRevenue AS (
    SELECT Country, SUM(Quantity * UnitPrice) as Revenue
    FROM retail_data
    GROUP BY Country
)
SELECT Country, Revenue,
       Revenue * 100.0 / SUM(Revenue) OVER() as pct_of_total
FROM CountryRevenue;
```

## 8. Rank Products by Revenue Within Category (Data: Rank Customers by Revenue Within Country)
```sql
WITH CustomerSpend AS (
    SELECT Country, CustomerID, SUM(Quantity * UnitPrice) as TotalSpend
    FROM retail_data
    WHERE CustomerID IS NOT NULL
    GROUP BY Country, CustomerID
)
SELECT Country, CustomerID, TotalSpend,
       RANK() OVER(PARTITION BY Country ORDER BY TotalSpend DESC) as rank_in_country
FROM CustomerSpend;
```

## 9. Find Duplicate Records
```sql
SELECT InvoiceNo, StockCode, Quantity
FROM (
    SELECT InvoiceNo, StockCode, Quantity,
           ROW_NUMBER() OVER(PARTITION BY InvoiceNo, StockCode ORDER BY Quantity DESC) as rn
    FROM retail_data
) WHERE rn > 1;
```

## 10. Gap Detection in IDs (Data: Time Gaps)
```sql
WITH CustomerDates AS (
    SELECT DISTINCT CAST(strptime(InvoiceDate, '%m/%d/%Y %-H:%M') AS DATE) as PurchaseDate
    FROM retail_data
    WHERE CustomerID = 17850
),
Gaps AS (
    SELECT PurchaseDate,
           CAST(PurchaseDate - LAG(PurchaseDate) OVER(ORDER BY PurchaseDate) AS INTEGER) as gap_days
    FROM CustomerDates
)
SELECT MAX(gap_days) as max_gap_days FROM Gaps;
```

## 11. Find Longest Streak of Activity
```sql
WITH DailyPurchases AS (
    SELECT DISTINCT CustomerID, CAST(strptime(InvoiceDate, '%m/%d/%Y %-H:%M') AS DATE) as PurchaseDate
    FROM retail_data
    WHERE CustomerID IS NOT NULL
),
Grouped AS (
    SELECT CustomerID, PurchaseDate,
           PurchaseDate - CAST(ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY PurchaseDate) AS INTEGER) AS grp
    FROM DailyPurchases
),
Streaks AS (
    SELECT CustomerID, grp, COUNT(*) as streak_length
    FROM Grouped
    GROUP BY CustomerID, grp
)
SELECT CustomerID, MAX(streak_length) as longest_streak
FROM Streaks
GROUP BY CustomerID
ORDER BY longest_streak DESC;
```

## 12. Sessionize User Activity
```sql
WITH Timestamps AS (
    SELECT DISTINCT InvoiceNo, strptime(InvoiceDate, '%m/%d/%Y %-H:%M') as EventTime
    FROM retail_data
    WHERE CustomerID = 17850
),
TimeDiffs AS (
    SELECT InvoiceNo, EventTime,
           date_diff('minute', LAG(EventTime) OVER(ORDER BY EventTime), EventTime) as mins_since_last
    FROM Timestamps
),
NewSessions AS (
    SELECT InvoiceNo, EventTime, mins_since_last,
           CASE WHEN mins_since_last > 60 OR mins_since_last IS NULL THEN 1 ELSE 0 END as is_new_session
    FROM TimeDiffs
)
SELECT InvoiceNo, EventTime, mins_since_last,
       SUM(is_new_session) OVER(ORDER BY EventTime) as session_id
FROM NewSessions;
```

## 13. Compare Current Row with Previous Row
```sql
WITH WeeklyRevenue AS (
    SELECT date_trunc('week', strptime(InvoiceDate, '%m/%d/%Y %-H:%M')) as WeekDate,
           SUM(Quantity * UnitPrice) as Revenue
    FROM retail_data
    GROUP BY WeekDate
)
SELECT WeekDate, Revenue,
       LAG(Revenue) OVER(ORDER BY WeekDate) as PrevRevenue,
       Revenue - LAG(Revenue) OVER(ORDER BY WeekDate) as RevenueGrowth
FROM WeeklyRevenue;
```

## 14. Identify First and Last Event Per User
```sql
WITH Ranked AS (
    SELECT CustomerID, StockCode, strptime(InvoiceDate, '%m/%d/%Y %-H:%M') as EventTime,
           FIRST_VALUE(StockCode) OVER(PARTITION BY CustomerID ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M')) as FirstProduct,
           LAST_VALUE(StockCode) OVER(PARTITION BY CustomerID ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M') ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as LastProduct
    FROM retail_data
    WHERE CustomerID IS NOT NULL
)
SELECT DISTINCT CustomerID, FirstProduct, LastProduct
FROM Ranked;
```

## 15. Top Performing Day per Store (Data: Top Day per Country)
```sql
WITH DailyCountryRev AS (
    SELECT Country, CAST(strptime(InvoiceDate, '%m/%d/%Y %-H:%M') AS DATE) as PrevDate,
           SUM(Quantity * UnitPrice) as Revenue
    FROM retail_data
    GROUP BY Country, PrevDate
),
RankedDays AS (
    SELECT Country, PrevDate, Revenue,
           ROW_NUMBER() OVER(PARTITION BY Country ORDER BY Revenue DESC) as rn
    FROM DailyCountryRev
)
SELECT Country, PrevDate as TopDay, Revenue
FROM RankedDays
WHERE rn = 1;
```

## 16. Percentile Ranking
```sql
WITH CustomerSpend AS (
    SELECT CustomerID, SUM(Quantity * UnitPrice) as TotalSpend
    FROM retail_data
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT CustomerID, TotalSpend,
       PERCENT_RANK() OVER(ORDER BY TotalSpend) as Percentile
FROM CustomerSpend;
```

## 17. Bucket Data into Groups
```sql
WITH CustomerSpend AS (
    SELECT CustomerID, SUM(Quantity * UnitPrice) as TotalSpend
    FROM retail_data
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
)
SELECT CustomerID, TotalSpend,
       NTILE(4) OVER(ORDER BY TotalSpend DESC) as SpendingTier
FROM CustomerSpend;
```

## 18. Find Products with Increasing Sales Trend
```sql
WITH MonthlySales AS (
    SELECT StockCode, date_trunc('month', strptime(InvoiceDate, '%m/%d/%Y %-H:%M')) as MonthYear,
           SUM(Quantity) as TotalQty
    FROM retail_data
    GROUP BY StockCode, MonthYear
),
SalesWithLag AS (
    SELECT StockCode, MonthYear, TotalQty,
           LAG(TotalQty) OVER(PARTITION BY StockCode ORDER BY MonthYear) as PrevQty
    FROM MonthlySales
)
SELECT StockCode, MonthYear, TotalQty, PrevQty
FROM SalesWithLag
WHERE TotalQty > PrevQty;
```

## 19. Running Balance Calculation
```sql
SELECT InvoiceNo, InvoiceDate, Quantity,
       SUM(Quantity) OVER(ORDER BY strptime(InvoiceDate, '%m/%d/%Y %-H:%M') ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as RunningQuantity
FROM retail_data
WHERE StockCode = '22423';
```

## 20. Detect Changes in Status
```sql
WITH CustomerCountries AS (
    SELECT DISTINCT CustomerID, InvoiceNo, strptime(InvoiceDate, '%m/%d/%Y %-H:%M') as EventTime, Country
    FROM retail_data
    WHERE CustomerID IS NOT NULL
),
CountryChanges AS (
    SELECT CustomerID, InvoiceNo, EventTime, Country,
           LAG(Country) OVER(PARTITION BY CustomerID ORDER BY EventTime) as PrevCountry
    FROM CustomerCountries
)
SELECT CustomerID, InvoiceNo, EventTime, PrevCountry, Country
FROM CountryChanges
WHERE PrevCountry IS NOT NULL AND Country != PrevCountry;
```
