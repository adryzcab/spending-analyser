import pandas as pd
import re


CATEGORY_RULES = {
    "Groceries": ["TESCO", "SAINSBURYS", "LIDL", "ICELAND"],
    "Transport": ["TFL", "UBER"],
    "Eating out": ["CAFE", "PRET", "NANDOS"],
    "Shopping": ["AMAZON"],
    "Utilities": ["GAS", "ELECTRIC", "WATER"],
    "Saving": ["SAVING"],
    "Rent": ["RENT"],
    "Travel": ["EASYJET"],
    "Entertainment": ["STEAM GAMES"],
    "Self care": ["BOOTS"],
    "Subscriptions": ["SPOTIFY", "NETFLIX"],
    "Transfer": ["WISE"],
    "Fees": ["NON-STERLING"],
}

TWO_WAY_CATEGORIES = ["Transfer"]

def categorise(description: str, amount: float) -> str:
    """Return the spending category for one transaction"""
    text = description.upper()
    for category in TWO_WAY_CATEGORIES:
        for keyword in CATEGORY_RULES[category]:
            if re.search(rf"\b{keyword}\b", text):
                return category
    if amount > 0:
        return "Income"
    for category, keywords in CATEGORY_RULES.items():
        for keyword in keywords:
            if re.search(rf"\b{keyword}\b", text):
                return category
    return "Other"

def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Return the DataFrame with a new 'category' column"""
    df["category"] = df.apply(
        lambda row: categorise(row["description"], row["amount"]),
        axis=1,
    )
    return df


