import pandas as pd




def without_transfer(df: pd.DataFrame) -> pd.DataFrame:
    """Return the transactions that aren't transfers between own accounts."""
    if "category" not in df.columns:
        return df
    return df[df["category"] != "Transfer"]

def spending_by_category(df: pd.DataFrame) -> pd.Series:
    """Return total spending per category, largest first.
    
    Expects a DataFrame with a 'category' column (see add_categories)
    """
    df = without_transfer(df)
    spending = df[df["amount"] < 0]
    by_category = spending.groupby("category")["amount"].sum()
    by_category = by_category.abs().sort_values(ascending=False)
    return by_category

def monthly_spending(df: pd.DataFrame) -> pd.Series:
    """Return total spending per month (positive numbers), oldest first."""
    df = without_transfer(df)
    spending = df[df["amount"] < 0]
    months = spending["date"].dt.to_period("M")
    totals = spending.groupby(months)["amount"].sum()
    return totals.abs().sort_index()

def monthly_change(df: pd.DataFrame) -> pd.Series:
    """Return change in spending vs the previous month (first month is NaN)."""
    totals = monthly_spending(df)
    return totals.diff()

def monthly_income(df: pd.DataFrame) -> pd.Series:
    """Return total income per month, oldest first."""
    df = without_transfer(df)
    income = df[df["amount"] > 0]
    months = income["date"].dt.to_period("M")
    totals = income.groupby(months)["amount"].sum()
    return totals.sort_index()

def monthly_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return income, spending and net per month, oldest first."""
    table = pd.DataFrame({
        "income": monthly_income(df),
        "spending": monthly_spending(df),
    })
    table = table.fillna(0)
    table["net"] = table["income"] - table["spending"]
    return table.sort_index()

def unusual_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Return spending that is unusually large for its category.
    
    Uses the IQR rule per category: a purchase is unusual if it's 
    above the category's 75th percentile + 1.5 * IQR
    """
    df = without_transfer(df)
    spending = df[df["amount"] < 0]
    sizes = spending["amount"].abs()
    limits = sizes.groupby(spending["category"]).transform(upper_limit)
    return spending[sizes > limits]

def upper_limit(amounts: pd.Series) -> float:
    """Return the IQR-rule upper limit for a set of amounts."""
    q1 = amounts.quantile(0.25)
    q3 = amounts.quantile(0.75)
    return q3 + 1.5 * (q3 - q1)

