import pandas as pd
import sqlite3

from spending_analyser.loader import load_hsbc_csv
from spending_analyser.categoriser import add_categories
from spending_analyser.storage import save_transactions


def ingest_hsbc_csvs(paths: list[str]) -> pd.DataFrame:
    """Load several HSBC CSVs into one DataFrame, without double-counting overlapping days."""
    frames = []
    for path in paths:
        df = load_hsbc_csv(path)
        frames.append(df)
    frames.sort(key=lambda df: df["date"].min())
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

def add_statement(path: str, conn: sqlite3.Connection) -> None:
    """Add one HSBC CSV to the database without duplicating stored rows.
    
    The CSV's last day is skipped because it may be incomplete; it is
    added from the next statement instead. Statement must overlap the 
    the database by at least one day, otherwise a ValueError is raised.
    """
    df = add_categories(load_hsbc_csv(path))
    latest = conn.execute("SELECT MAX(date) FROM transactions").fetchone()[0]
    if latest is not None:
        latest = pd.Timestamp(latest)
    if latest is not None and df["date"].min() > latest:
        raise ValueError(
            f"Statement starts {df['date'].min():%Y-%m-%d}, after the latest stored "
            f"date {latest:%Y-%m-%d}. Download a statement starting on or before "
            f"{latest:%Y-%m-%d}."
        )
    df = df[df["date"] < df["date"].max()]
    if latest is not None:
        df = df[df["date"] > latest]
    save_transactions(df, conn)