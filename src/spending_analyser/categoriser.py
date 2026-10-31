import pandas as pd


CATEGORY_RULES = {
    "Groceries": ["TESCO", "SAINSBURY"],
    "Transport": ["TFL", "UBER"],
    "Eating out": ["CAFE", "PRET"],
    "Shopping": ["AMAZON"],
    "Utilities": ["GAS", "ELECTRIC", "WATER"],
    "Saving": ["SAVING"],
    "Rent": ["RENT"],
    "Travel": ["EASYJET"]
}

def categorise(description: str, amount: float) -> str:
    """Return the spending category for one transaction"""
    if amount > 0:
        return "Income"
    
    text = description.upper()
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if keyword in text:
                return category

    return "Other"

def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Return the DataFrame with a new 'category' column"""
    df["category"] = df.apply(
        lambda row: categorise(row["description"], row["amount"]),
        axis=1,
    )
    return df


