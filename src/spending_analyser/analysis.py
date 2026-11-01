import pandas as pd





def spending_by_category(df: pd.DataFrame) -> pd.Series:
    """Return total spending per category, largest first.
    
    Expects a DataFrame with a 'category' column (see add_categories)
    """
    spending = df[df["amount"] < 0]
    by_category = spending.groupby("category")["amount"].sum()
    by_category = by_category.abs().sort_values(ascending=False)
    return by_category