"""
value_functions/validators.py — Shared validation logic for Value Functions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This file contains the validation functions for all exercises in the 
value_functions module. This ensures that both exercises and solutions
share exactly the same validation logic.
"""

# LAG() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_lag_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "quantity", "prev_quantity"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    null_count = df["prev_quantity"].isna().sum()
    if null_count == 0:
        return False, "Expected some NULL values in prev_quantity (first purchase per customer has no prior row)."
    if (df["prev_quantity"].dropna() == df.loc[df["prev_quantity"].notna(), "quantity"]).all():
        return (
            False,
            "prev_quantity appears to equal quantity for every row — "
            "make sure you are using LAG() not just copying the column.",
        )
    return True, f"LAG correctly applied — {null_count} NULL first-purchase rows detected."


def validate_lag_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "revenue", "prev_revenue", "revenue_delta"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["prev_revenue"].isna().any():
        return False, "prev_revenue has NULL values — use LAG with a default of 0 for the first invoice."
    computed = (df["revenue"] - df["prev_revenue"]).round(2)
    actual = df["revenue_delta"].round(2)
    if not (abs(computed - actual) < 0.05).all():
        return False, "revenue_delta does not equal revenue − prev_revenue for all rows."
    return True, f"Revenue delta correctly computed for {df['customerid'].nunique()} customers."


def validate_lag_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "country", "prev_country"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["prev_country"].isna().any():
        return False, "Result contains NULL prev_country — filter those rows out (they are first purchases)."
    mismatches = (df["country"] == df["prev_country"]).sum()
    if mismatches > 0:
        return False, f"{mismatches} rows have country = prev_country — only include rows where the country changed."
    return True, f"Found {len(df)} invoice lines where a customer switched country between purchases."


# LEAD() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_lead_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "next_invoice_no"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    null_count = df["next_invoice_no"].isna().sum()
    if null_count == 0:
        return False, "Expected NULL values in next_invoice_no for each customer's last invoice."
    non_null = df["next_invoice_no"].dropna()
    if (non_null == df.loc[df["next_invoice_no"].notna(), "invoiceno"]).all():
        return False, "next_invoice_no equals invoiceno for all non-null rows — LEAD() is not being applied correctly."
    return True, f"LEAD correctly applied — {null_count} final-invoice NULL rows detected."


def validate_lead_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoice_day", "invoiceno", "next_invoice_day", "days_until_next"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    null_count = df["days_until_next"].isna().sum()
    if null_count == 0:
        return False, "Expected NULL days_until_next for each customer's final invoice."
    non_null_days = df["days_until_next"].dropna()
    if (non_null_days < 0).any():
        return False, "Some days_until_next values are negative — check ORDER BY direction."
    return True, (
        f"days_until_next correctly computed. "
        f"Average gap: {non_null_days.mean():.1f} days across {df['customerid'].nunique()} customers."
    )


def validate_lead_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["customerid"].duplicated().any():
        return False, "Duplicate CustomerIDs found — each customer should appear at most once."
    return True, f"Penultimate invoice correctly identified for {len(df)} customers."


# FIRST_VALUE() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_first_value_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "stockcode", "first_stockcode"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["first_stockcode"].isna().any():
        return False, "first_stockcode has NULL values — check your ROWS frame clause."
    multi = df.groupby("customerid")["first_stockcode"].nunique()
    bad = (multi > 1).sum()
    if bad > 0:
        return False, f"{bad} customers have more than one distinct first_stockcode — FIRST_VALUE() not applied correctly."
    return True, f"first_stockcode correctly assigned for {df['customerid'].nunique()} customers."


def validate_first_value_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "cheapest_in_country"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["cheapest_in_country"].isna().any():
        return False, "cheapest_in_country has NULL values — add the ROWS frame clause."
    country_min = df.groupby("country")["avg_price"].min().rename("expected_min")
    merged = df.merge(country_min, on="country")
    if not (abs(merged["cheapest_in_country"] - merged["expected_min"]) < 0.01).all():
        return False, "cheapest_in_country does not match the actual minimum avg_price per country."
    return True, f"cheapest_in_country correctly computed across {df['country'].nunique()} countries."


def validate_first_value_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoice_day", "invoiceno", "first_purchase_day", "days_since_first"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["days_since_first"].isna().any():
        return False, "days_since_first has NULL values — check the frame clause for FIRST_VALUE."
    if (df["days_since_first"] < 0).any():
        return False, "Some days_since_first values are negative — ensure you subtract first from current."
    zero_rows = (df["days_since_first"] == 0).sum()
    if zero_rows == 0:
        return False, "No rows with days_since_first = 0 — every customer's first row should be 0."
    return True, (
        f"days_since_first correctly computed. "
        f"{zero_rows} rows at day 0 (first purchases) across {df['customerid'].nunique()} customers."
    )


# LAST_VALUE() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_last_value_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoicedate", "invoiceno", "stockcode", "last_stockcode"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["last_stockcode"].isna().any():
        return False, "last_stockcode has NULL values — add the ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING frame."
    multi = df.groupby("customerid")["last_stockcode"].nunique()
    bad = (multi > 1).sum()
    if bad > 0:
        return False, f"{bad} customers have >1 distinct last_stockcode — frame clause may be missing."
    return True, f"last_stockcode correctly assigned for {df['customerid'].nunique()} customers."


def validate_last_value_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "priciest_in_country"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["priciest_in_country"].isna().any():
        return False, "priciest_in_country has NULL values — add the ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING frame."
    country_max = df.groupby("country")["avg_price"].max().rename("expected_max")
    merged = df.merge(country_max, on="country")
    if not (abs(merged["priciest_in_country"] - merged["expected_max"]) < 0.01).all():
        return False, "priciest_in_country does not match the actual maximum avg_price per country."
    return True, f"priciest_in_country correctly computed across {df['country'].nunique()} countries."


def validate_last_value_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "invoice_day", "invoiceno", "first_purchase_day", "last_purchase_day", "lifetime_days"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["lifetime_days"].isna().any():
        return False, "lifetime_days has NULL values — check frame clauses for both FIRST_VALUE and LAST_VALUE."
    if (df["lifetime_days"] < 0).any():
        return False, "Some lifetime_days are negative — ensure first_purchase_day <= last_purchase_day."
    one_purchase = df.groupby("customerid")["invoice_day"].nunique()
    single = one_purchase[one_purchase == 1].index
    if len(single) > 0:
        check = df[df["customerid"].isin(single)]["lifetime_days"]
        if (check != 0).any():
            return False, "Customers with only one purchase date should have lifetime_days = 0."
    return True, (
        f"lifetime_days correctly computed for {df['customerid'].nunique()} customers. "
        f"Median lifetime: {df['lifetime_days'].median():.0f} days."
    )
