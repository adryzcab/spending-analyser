import pandas as pd





def spending_by_category(df: pd.DataFrame) -> pd.Series:
    """Return total spending per category, largest first.
    
    Expects a DataFrame with a 'category' column (see add_categories)
    """
    spending = df[df["amount"] < 0]
    by_category = spending.groupby("category")["amount"].sum()
    by_category = by_category.abs().sort_values(ascending=False)
    return by_category

def monthly_spending(df: pd.DataFrame) -> pd.Series:
    """Return total spending per month (positive numbers), oldest first."""
    spending = df[df["amount"] < 0]
    months = spending["date"].dt.to_period("M")
    totals = spending.groupby(months)["amount"].sum()
    return totals.abs().sort_index()

def monthly_change(df: pd.DataFrame) -> pd.Series:
    """Return change in spending vs the previous month (first month is NaN)."""
    totals = monthly_spending(df)
    return totals.diff()