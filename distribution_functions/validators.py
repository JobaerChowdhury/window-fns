"""
distribution_functions/validators.py — Shared Validation Logic
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This file contains the shared validate_exN functions used by both
exercises/ and solutions/ in the distribution_functions module.
"""

# ════════════════════════════════════════════════════════════════════════════
# NTILE() Validators
# ════════════════════════════════════════════════════════════════════════════

def validate_ntile_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "total_qty", "qty_quartile"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["qty_quartile"].isna().any():
        return False, "qty_quartile has NULL values."
    # Must have exactly 4 distinct quartile values
    unique_quartiles = set(df["qty_quartile"].unique())
    if not unique_quartiles <= {1, 2, 3, 4}:
        return False, f"qty_quartile values must be 1–4, got {unique_quartiles}."
    if len(unique_quartiles) < 2:
        return False, "Expected multiple quartile values — check NTILE(4)."
    return True, (
        f"qty_quartile correctly assigned across {df['country'].nunique()} countries."
    )

def validate_ntile_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "total_spend", "spend_quintile"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["spend_quintile"].isna().any():
        return False, "spend_quintile has NULL values."
    # All rows must be quintile 5
    if (df["spend_quintile"] != 5).any():
        return False, "Not all rows are in quintile 5 — filter WHERE spend_quintile = 5."
    if df["customerid"].nunique() < 10:
        return False, "Expected more than 10 customers in the top quintile."
    return True, (
        f"{df['customerid'].nunique()} top-quintile customers correctly identified."
    )

def validate_ntile_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "price_tier", "tier_label"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["price_tier"].isna().any():
        return False, "price_tier has NULL values."
    if df["tier_label"].isna().any():
        return False, "tier_label has NULL values — check CASE expression."
    # Tier labels must be one of three expected values
    expected_labels = {"Budget", "Mid-Range", "Premium"}
    actual_labels = set(df["tier_label"].unique())
    if not actual_labels <= expected_labels:
        return False, f"Unexpected tier_label values: {actual_labels - expected_labels}."
    # price_tier must be 1, 2, or 3
    if not set(df["price_tier"].unique()) <= {1, 2, 3}:
        return False, "price_tier should only contain 1, 2, or 3."
    return True, (
        f"price_tier and tier_label correctly assigned across "
        f"{df['country'].nunique()} countries."
    )

# ════════════════════════════════════════════════════════════════════════════
# CUME_DIST() Validators
# ════════════════════════════════════════════════════════════════════════════

def validate_cume_dist_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "country_revenue", "cume_dist"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["cume_dist"].isna().any():
        return False, "cume_dist has NULL values."
    # cume_dist must be in (0, 1]
    if (df["cume_dist"] <= 0).any() or (df["cume_dist"] > 1.0001).any():
        return False, "cume_dist values must be in the range (0, 1]."
    # Last row (highest revenue) must have cume_dist = 1.0
    if abs(df["cume_dist"].max() - 1.0) > 0.001:
        return False, "The maximum cume_dist value must be 1.0."
    return True, (
        f"cume_dist correctly computed for {df['country'].nunique()} countries."
    )

def validate_cume_dist_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "total_spend", "cume_dist"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["cume_dist"].isna().any():
        return False, "cume_dist has NULL values."
    # All returned cume_dist values must be >= 0.8
    if (df["cume_dist"] < 0.79).any():
        return False, "Some returned rows have cume_dist < 0.80 — filter WHERE cume_dist >= 0.8."
    if df["customerid"].nunique() < 10:
        return False, "Expected more than 10 customers in the top 20%."
    return True, (
        f"{df['customerid'].nunique()} customers correctly identified in the top 20% by spend."
    )

def validate_cume_dist_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "cume_dist", "is_cheap"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["cume_dist"].isna().any():
        return False, "cume_dist has NULL values."
    if df["is_cheap"].isna().any():
        return False, "is_cheap has NULL values."
    if df["country"].nunique() != 3:
        return False, f"Expected exactly 3 countries, got {df['country'].nunique()}."
    # Rows with cume_dist <= 0.25 should be flagged True
    cheap_mask = df["cume_dist"] <= 0.25
    if not (df.loc[cheap_mask, "is_cheap"].all()):
        return False, "Rows with cume_dist <= 0.25 should have is_cheap = True."
    return True, (
        f"is_cheap correctly flagged across {df['country'].nunique()} countries."
    )

# ════════════════════════════════════════════════════════════════════════════
# PERCENT_RANK() Validators
# ════════════════════════════════════════════════════════════════════════════

def validate_percent_rank_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "order_count", "pct_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["pct_rank"].isna().any():
        return False, "pct_rank has NULL values."
    # First row must be 0.0
    if abs(df["pct_rank"].min()) > 0.001:
        return False, "The minimum pct_rank must be 0.0 (first row, ORDER BY ASC)."
    # Last row must be 1.0
    if abs(df["pct_rank"].max() - 1.0) > 0.001:
        return False, "The maximum pct_rank must be 1.0."
    # Must be in [0, 1]
    if (df["pct_rank"] < 0).any() or (df["pct_rank"] > 1.0001).any():
        return False, "pct_rank values must be in [0, 1]."
    return True, (
        f"pct_rank correctly computed for {df['country'].nunique()} countries."
    )

def validate_percent_rank_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "modal_country", "total_spend", "pct_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if df["pct_rank"].isna().any():
        return False, "pct_rank has NULL values."
    if (df["pct_rank"] < 0).any() or (df["pct_rank"] > 1.0001).any():
        return False, "pct_rank values must be in [0, 1]."
    # Each country group should have at least one row with pct_rank = 0.0
    first_rows = df.groupby("modal_country")["pct_rank"].min()
    if (abs(first_rows) > 0.01).any():
        return False, "Each country group should have a pct_rank starting near 0.0."
    return True, (
        f"pct_rank correctly partitioned by modal_country across "
        f"{df['modal_country'].nunique()} countries."
    )

def validate_percent_rank_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"customerid", "total_spend", "ntile_quartile", "cume_dist", "pct_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    for col in ("cume_dist", "pct_rank"):
        if df[col].isna().any():
            return False, f"{col} has NULL values."
    if df["ntile_quartile"].isna().any():
        return False, "ntile_quartile has NULL values."
    # ntile must only contain 1-4
    if not set(df["ntile_quartile"].unique()) <= {1, 2, 3, 4}:
        return False, "ntile_quartile should only contain values 1–4."
    # cume_dist and pct_rank in [0,1]
    if (df["cume_dist"] <= 0).any() or (df["cume_dist"] > 1.0001).any():
        return False, "cume_dist must be in range (0, 1]."
    if (df["pct_rank"] < 0).any() or (df["pct_rank"] > 1.0001).any():
        return False, "pct_rank must be in range [0, 1]."
    return True, (
        "All three distribution functions (NTILE, CUME_DIST, PERCENT_RANK) "
        f"correctly computed for {df['customerid'].nunique()} customers."
    )
