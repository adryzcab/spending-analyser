import sqlite3

import pandas as pd

def create_table(conn: sqlite3.Connection) -> None:
    """Create the transaction table if it doesn't exist."""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY,
        date TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        category_source TEXT CHECK (category_source IN ('rule', 'manual'))
    )
""")

def save_transactions(df: pd.DataFrame, conn:sqlite3.Connection) -> None:
    """Save transactions to the database."""
    rows = df.copy()
    rows["date"] = rows["date"].dt.strftime("%Y-%m-%d")
    rows["category_source"] = "rule"
    rows = rows[["date", "description", "amount", "category", "category_source"]]
    rows.to_sql("transactions", conn, if_exists="append", index=False)

def load_transactions(conn: sqlite3.Connection) -> pd.DataFrame:
    """Load all transactions from the database"""
    return pd.read_sql(
        "SELECT * FROM transactions ORDER BY date, id",
        conn,
        parse_dates=["date"]
    )