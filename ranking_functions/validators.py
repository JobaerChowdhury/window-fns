"""
ranking_functions/validators.py — Shared validation logic for Ranking Functions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This file contains the validation functions for all exercises in the 
ranking_functions module. This ensures that both exercises and solutions
share exactly the same validation logic.
"""

# ROW_NUMBER() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_row_number_ex1(df):
    if "row_num" not in df.columns:
        return False, "Column 'row_num' not found in result."
    if "country" not in [c.lower() for c in df.columns]:
        return False, "Column 'Country' not found in result."
    df.columns = [c.lower() for c in df.columns]
    rank1 = df[df["row_num"] == 1]
    if rank1["country"].duplicated().any():
        return False, "Some countries appear more than once with row_num = 1."
    max_qty = df.groupby("country")["quantity"].max().reset_index().rename(columns={"quantity": "max_qty"})
    merged = rank1.merge(max_qty, on="country")
    if not (merged["quantity"] == merged["max_qty"]).all():
        return False, "Row with row_num=1 does not always have the highest Quantity for its Country."
    return True, "Row number 1 correctly identifies the highest-quantity line per country."


def validate_row_number_ex2(df):
    if df.empty:
        return False, "Result is empty — make sure you filter for purchase_num = 2."
    df.columns = [c.lower() for c in df.columns]
    if "purchase_num" not in df.columns:
        return False, "Column 'purchase_num' not found."
    if not (df["purchase_num"] == 2).all():
        return False, "Not all rows have purchase_num = 2."
    if df["customerid"].duplicated().any():
        return False, "Duplicate CustomerIDs found — each customer should appear once."
    return True, f"Correctly found the 2nd purchase for {len(df)} customers."


def validate_row_number_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    if "invoiceno" not in df.columns or "stockcode" not in df.columns:
        return False, "Expected columns 'InvoiceNo' and 'StockCode' not found."
    dupes = df.duplicated(subset=["invoiceno", "stockcode"])
    if dupes.any():
        return False, f"{dupes.sum()} duplicate (InvoiceNo, StockCode) pairs remain — filter to rn = 1."
    return True, f"No duplicate (InvoiceNo, StockCode) pairs — {len(df):,} unique rows."


# RANK() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_rank_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "unique_customers", "country_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    top = df[df["country_rank"] == 1]
    if top.empty:
        return False, "No row with country_rank = 1 found."
    countries_at_1 = top["country"].str.strip().str.lower().tolist()
    if "united kingdom" not in countries_at_1:
        return False, f"Expected 'United Kingdom' at rank 1, got: {countries_at_1}"
    return True, "United Kingdom is correctly ranked 1 by unique customer count."


def validate_rank_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "price_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    rank1 = df[df["price_rank"] == 1]
    max_price = df.groupby("country")["avg_price"].max().reset_index().rename(columns={"avg_price": "max_price"})
    merged = rank1.merge(max_price, on="country")
    if not (merged["avg_price"] >= merged["max_price"] * 0.999).all():
        return False, "Rank 1 does not always correspond to the highest avg_price within a Country."
    return True, f"price_rank correctly assigned across {df['country'].nunique()} countries."


def validate_rank_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"stockcode", "total_qty", "rn", "pos_rank", "dense_pos"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if len(df) != 15:
        return False, f"Expected exactly 15 rows, got {len(df)}."
    if sorted(df["rn"].tolist()) != list(range(1, 16)):
        return False, "ROW_NUMBER (rn) must be 1–15 with no duplicates."
    if df["pos_rank"].min() != 1:
        return False, "RANK (pos_rank) must start at 1."
    if df["dense_pos"].min() != 1:
        return False, "DENSE_RANK (dense_pos) must start at 1."
    dense_vals = sorted(df["dense_pos"].unique().tolist())
    expected_dense = list(range(1, dense_vals[-1] + 1))
    if dense_vals != expected_dense:
        return False, (
            f"DENSE_RANK (dense_pos) has gaps — got {dense_vals}. "
            "Make sure you used DENSE_RANK(), not RANK()."
        )
    if not (df["pos_rank"] >= df["dense_pos"]).all():
        return False, "RANK should always be >= DENSE_RANK for the same ordering."
    has_tie = df.duplicated(subset=["total_qty"]).any()
    tie_note = (
        "Ties detected — compare rn, pos_rank, and dense_pos: "
        "rn is always unique, pos_rank SKIPS after a tie, dense_pos stays contiguous. ✓"
        if has_tie else
        "No ties in these 15 rows."
    )
    return True, f"All 15 rows correct. {tie_note}"


# DENSE_RANK() Validators
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def validate_dense_rank_ex1(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "total_sales", "sales_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    top = df[df["sales_rank"] == 1]
    countries_at_1 = top["country"].str.strip().str.lower().tolist()
    if "united kingdom" not in countries_at_1:
        return False, f"Expected 'United Kingdom' at rank 1, got: {countries_at_1}"
    ranks = sorted(df["sales_rank"].unique())
    expected = list(range(1, len(ranks) + 1))
    if ranks != expected:
        return False, (
            f"Ranks are not contiguous — found gaps. Got: {ranks[:10]}... "
            "Make sure you're using DENSE_RANK, not RANK."
        )
    return True, f"UK is rank 1 and all {len(ranks)} ranks are contiguous — no gaps! ✓"


def validate_dense_rank_ex2(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"country", "stockcode", "avg_price", "price_rank"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    rank1 = df[df["price_rank"] == 1]
    min_price = df.groupby("country")["avg_price"].min().reset_index().rename(columns={"avg_price": "min_price"})
    merged = rank1.merge(min_price, on="country")
    if not (merged["avg_price"] <= merged["min_price"] * 1.001).all():
        return False, "Rank 1 does not correspond to the lowest avg_price per country — check ORDER BY direction (ASC)."
    return True, f"Rank 1 correctly identifies the cheapest product per country across {df['country'].nunique()} countries."


def validate_dense_rank_ex3(df):
    if df.empty:
        return False, "Result is empty."
    df.columns = [c.lower() for c in df.columns]
    required = {"stockcode", "num_orders", "rn", "cust_rank", "dense_cust"}
    missing = required - set(df.columns)
    if missing:
        return False, f"Missing columns: {missing}"
    if len(df) != 15:
        return False, f"Expected exactly 15 rows, got {len(df)}."
    if sorted(df["rn"].tolist()) != list(range(1, 16)):
        return False, "ROW_NUMBER (rn) must be 1–15 with no duplicates."
    if df["cust_rank"].min() != 1:
        return False, "RANK (cust_rank) must start at 1."
    if df["dense_cust"].min() != 1:
        return False, "DENSE_RANK (dense_cust) must start at 1."
    if not (df["cust_rank"] >= df["dense_cust"]).all():
        return False, "RANK should always be >= DENSE_RANK for the same ordering."
    dense_vals = sorted(df["dense_cust"].unique().tolist())
    expected_dense = list(range(1, dense_vals[-1] + 1))
    if dense_vals != expected_dense:
        return False, (
            f"DENSE_RANK (dense_cust) has gaps — got {dense_vals}. "
            "Make sure you used DENSE_RANK(), not RANK()."
        )
    has_tie = df.duplicated(subset=["num_orders"]).any()
    if not has_tie:
        return False, "No ties found — check your query targets Germany and uses COUNT(DISTINCT InvoiceNo)."
    if not (df["cust_rank"].max() > df["dense_cust"].max()):
        return False, (
            f"RANK max ({df['cust_rank'].max()}) should exceed DENSE_RANK max ({df['dense_cust'].max()}) "
            "when ties are present. Check that cust_rank uses RANK() and dense_cust uses DENSE_RANK()."
        )
    return True, (
        f"All 15 rows correct. Ties found! "
        f"RANK max = {df['cust_rank'].max()} vs DENSE_RANK max = {df['dense_cust'].max()} — "
        f"RANK skips {df['cust_rank'].max() - df['dense_cust'].max()} number(s), DENSE_RANK stays contiguous. ✓"
    )
