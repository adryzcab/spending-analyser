import pandas as pd


def load_hsbc_csv(path: str) -> pd.DataFrame:
    """Load an HSBC transactions CSV and return a clean DataFrame."""
    df = pd.read_csv(
        path,
        header=None,
        names=["date", "description", "amount"],
        thousands=","
    )
    df["date"] = pd.to_datetime(df["date"], format="%d/%m/%Y")
    return df