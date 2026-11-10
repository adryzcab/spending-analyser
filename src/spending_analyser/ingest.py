import pandas as pd

from spending_analyser.loader import load_hsbc_csv


def ingest_hsbc_csvs(paths: list[str]) -> pd.DataFrame:
    """Load several HSBC CSVs into one DataFrame, without double-counting overlapping days."""
    frames = []
    for path in paths:
        df = load_hsbc_csv(path)
        frames.append(df)
    first = frames[0]
    last_date = first["date"].max()
    first = first[first["date"] < last_date]
    second = frames[1]
    second = second[second["date"] >= last_date]
    return pd.concat([first, second], ignore_index=True)