"""
aggregate_functions/validators.py — Shared validation logic for Aggregate Functions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This file contains the validation functions for all exercises in the 
aggregate_functions module. This ensures that both exercises and solutions
share exactly the same validation logic.
"""

# SUM() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_sum_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "invoiceno", "stockcode", "line_revenue", "country_total", "grand_total"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["country_total"].isna().any():
        return False, "country_total has NULL values."
    if df["grand_total"].isna().any():
        return False, "grand_total has NULL values."
    # grand_total should be the same on every row
    if df["grand_total"].nunique() != 1:
        return False, "grand_total is not the same on every row — use SUM() OVER() with no partition."
    # country_total must be <= grand_total
    if (df["country_total"] > df["grand_total"] + 0.01).any():
        return False, "country_total exceeds grand_total — check partition logic."
    return True, (
        f"grand_total and country_total correctly computed across "
        f"{df['country'].nunique()} countries."
    )


def validate_sum_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "cumulative_revenue"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["cumulative_revenue"].isna().any():
        return False, "cumulative_revenue has NULL values."
    # cumulative_revenue must be monotonically non-decreasing per customer
    df_sorted = df.sort_values(["customerid", "invoicedate"])
    bad = (
        df_sorted.groupby("customerid")["cumulative_revenue"]
        .apply(lambda s: (s.diff().dropna() < -0.01).any())
    )
    if bad.any():
        return False, "cumulative_revenue decreases for some customers — ensure ORDER BY InvoiceDate."
    return True, (
        f"Running cumulative revenue correctly computed for "
        f"{df['customerid'].nunique()} customers."
    )


def validate_sum_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "customer_total", "pct_of_total"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["pct_of_total"].isna().any():
        return False, (
            "pct_of_total has NULL values — add a CTE that computes customer_total first, "
            "then filter WHERE customer_total > 0 before dividing."
        )
    # pct_of_total must be between 0 and 100
    if (df["pct_of_total"] < 0).any() or (df["pct_of_total"] > 100.1).any():
        return False, "pct_of_total values are outside [0, 100]."
    # For each customer, percentages should sum roughly to 100
    totals = df.groupby("customerid")["pct_of_total"].sum()
    bad = totals[abs(totals - 100) > 1]
    if len(bad) > 0:
        return False, f"{len(bad)} customers have pct_of_total not summing to ~100."
    return True, (
        f"pct_of_total correctly computed for {df['customerid'].nunique()} customers."
    )


# AVG() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_avg_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "unitprice", "country_avg_price", "global_avg_price"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["country_avg_price"].isna().any():
        return False, "country_avg_price has NULL values."
    if df["global_avg_price"].isna().any():
        return False, "global_avg_price has NULL values."
    # global_avg_price must be the same on every row
    if df["global_avg_price"].nunique() != 1:
        return False, "global_avg_price is not the same on every row — use AVG() OVER() with no partition."
    return True, (
        f"country_avg_price and global_avg_price correctly computed across "
        f"{df['country'].nunique()} countries."
    )


def validate_avg_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "running_avg", "spend_trend"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["running_avg"].isna().any():
        return False, "running_avg has NULL values."
    valid_trends = {"above_avg", "below_avg", "at_avg"}
    unexpected = set(df["spend_trend"].dropna().unique()) - valid_trends - {""}
    if unexpected:
        return False, f"Unexpected spend_trend values: {unexpected}. Expected 'above_avg' or 'below_avg'."
    return True, (
        f"running_avg and spend_trend correctly computed for "
        f"{df['customerid'].nunique()} customers."
    )


def validate_avg_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "avg_all_time", "moving_avg_3"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["moving_avg_3"].isna().any():
        return False, "moving_avg_3 has NULL values."
    if df["avg_all_time"].isna().any():
        return False, "avg_all_time has NULL values."
    # avg_all_time must be constant per customer
    bad = (
        df.groupby("customerid")["avg_all_time"].nunique()
    )
    multi = (bad > 1).sum()
    if multi > 0:
        return False, f"{multi} customers have varying avg_all_time — use PARTITION BY CustomerID with no ORDER BY."
    return True, (
        f"3-invoice moving average correctly computed for "
        f"{df['customerid'].nunique()} customers."
    )


# COUNT() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_count_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "invoiceno", "stockcode", "country_row_count", "global_row_count"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    # global_row_count must be the same everywhere
    if df["global_row_count"].nunique() != 1:
        return False, "global_row_count differs across rows — use COUNT(*) OVER() with no partition."
    # country_row_count must be <= global_row_count
    if (df["country_row_count"] > df["global_row_count"]).any():
        return False, "country_row_count exceeds global_row_count."
    return True, (
        f"country_row_count and global_row_count correctly attached across "
        f"{df['country'].nunique()} countries."
    )


def validate_count_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "stockcode", "row_seq"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["row_seq"].isna().any():
        return False, "row_seq has NULL values."
    # row_seq must start at 1 for each customer and be non-decreasing
    min_seq = df.groupby("customerid")["row_seq"].min()
    if (min_seq < 1).any():
        return False, "row_seq should start at 1 for each customer."
    return True, (
        f"row_seq correctly computed for {df['customerid'].nunique()} customers."
    )


def validate_count_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "invoiceno", "customerid", "identified_rows", "total_rows", "pct_identified"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["pct_identified"].isna().any():
        return False, "pct_identified has NULL values."
    if (df["pct_identified"] < 0).any() or (df["pct_identified"] > 100.1).any():
        return False, "pct_identified out of range [0, 100]."
    if (df["identified_rows"] > df["total_rows"]).any():
        return False, "identified_rows exceeds total_rows."
    return True, (
        f"pct_identified correctly computed across {df['country'].nunique()} countries."
    )


# MIN() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_min_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "description", "unitprice", "country_min_price", "global_min_price"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    # global_min_price must be the same everywhere
    if df["global_min_price"].nunique() != 1:
        return False, "global_min_price is not the same on every row — use MIN() OVER() with no partition."
    # country_min_price must be >= global_min_price
    if (df["country_min_price"] < df["global_min_price"] - 0.01).any():
        return False, "country_min_price is less than global_min_price — check partition logic."
    return True, (
        f"country_min_price and global_min_price correctly computed across "
        f"{df['country'].nunique()} countries."
    )


def validate_min_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "running_min_revenue"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["running_min_revenue"].isna().any():
        return False, "running_min_revenue has NULL values."
    # running_min_revenue <= invoice_revenue
    if (df["running_min_revenue"] > df["invoice_revenue"] + 0.01).any():
        return False, "running_min_revenue exceeds invoice_revenue for some rows — check the window."
    # running_min_revenue must be non-increasing per customer over time
    df_sorted = df.sort_values(["customerid", "invoicedate"])
    bad = (
        df_sorted.groupby("customerid")["running_min_revenue"]
        .apply(lambda s: (s.diff().dropna() > 0.01).any())
    )
    if bad.any():
        return False, "running_min_revenue increases for some customers — it should never increase."
    return True, (
        f"Running minimum correctly computed for {df['customerid'].nunique()} customers."
    )


def validate_min_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "first_purchase_date", "days_since_first"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["days_since_first"].isna().any():
        return False, "days_since_first has NULL values."
    if (df["days_since_first"] < 0).any():
        return False, (
            "days_since_first is negative — InvoiceDate is a string so MIN() on it uses "
            "lexicographic order. Parse to a timestamp in a CTE first: "
            "STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_ts, then MIN(invoice_ts) OVER()."
        )
    # first_purchase_date should be constant per customer
    bad = df.groupby("customerid")["first_purchase_date"].nunique()
    if (bad > 1).any():
        return False, "first_purchase_date is not constant per customer."
    return True, (
        f"first_purchase_date and days_since_first correctly computed "
        f"for {df['customerid'].nunique()} customers."
    )


# MAX() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_max_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "description", "unitprice", "country_max_price", "global_max_price"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["global_max_price"].nunique() != 1:
        return False, "global_max_price is not the same on every row — use MAX() OVER() with no partition."
    if (df["country_max_price"] > df["global_max_price"] + 0.01).any():
        return False, "country_max_price exceeds global_max_price — check partition logic."
    return True, (
        f"country_max_price and global_max_price correctly computed across "
        f"{df['country'].nunique()} countries."
    )


def validate_max_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "invoice_revenue", "running_max_revenue", "is_record"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["running_max_revenue"].isna().any():
        return False, "running_max_revenue has NULL values."
    # running_max_revenue >= invoice_revenue always
    if (df["running_max_revenue"] < df["invoice_revenue"] - 0.01).any():
        return False, "running_max_revenue is less than invoice_revenue — running max must be >= current value."
    # running_max_revenue must be non-decreasing per customer
    df_sorted = df.sort_values(["customerid", "invoicedate"])
    bad = (
        df_sorted.groupby("customerid")["running_max_revenue"]
        .apply(lambda s: (s.diff().dropna() < -0.01).any())
    )
    if bad.any():
        return False, "running_max_revenue decreases for some customers — it should never decrease."
    return True, (
        f"Running maximum correctly computed for {df['customerid'].nunique()} customers."
    )


def validate_max_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "last_purchase_date", "days_until_last"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["days_until_last"].isna().any():
        return False, "days_until_last has NULL values."
    if (df["days_until_last"] < 0).any():
        return False, (
            "days_until_last is negative — InvoiceDate is a string so MAX() on it uses "
            "lexicographic order. Parse to a timestamp in a CTE first: "
            "STRPTIME(InvoiceDate, '%m/%d/%Y %H:%M') AS invoice_ts, then MAX(invoice_ts) OVER()."
        )
    # last_purchase_date must be constant per customer
    bad = df.groupby("customerid")["last_purchase_date"].nunique()
    if (bad > 1).any():
        return False, "last_purchase_date is not constant per customer."
    return True, (
        f"last_purchase_date and days_until_last correctly computed "
        f"for {df['customerid'].nunique()} customers."
    )
