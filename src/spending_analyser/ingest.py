import pandas as pd

from spending_analyser.loader import load_hsbc_csv


def ingest_hsbc_csvs(paths: list[str]) -> pd.DataFrame:
    """Load several HSBC CSVs into one DataFrame, without double-counting overlapping days."""
    frames = []
    for path in paths:
        df = load_hsbc_csv(path)
        frames.append(df)
    kept = []
    for i in range(len(frames)):
        frame = frames[i]
        if i != 0:
            previous = frames[i -1]
            last_date = previous["date"].max()
            frame = frame[frame["date"] >= last_date]
        if i != len(frames) -1:
            own_last = frame["date"].max()
            frame = frame[frame["date"] < own_last]
        kept.append(frame)
    return pd.concat(kept, ignore_index=True)