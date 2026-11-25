import sqlite3

import pandas as pd

from spending_analyser.categoriser import categorise

COLUMNS = """
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT,
    category_source TEXT CHECK(category_source in ('rule', 'manual', 'model'))
"""


def create_table(conn: sqlite3.Connection) -> None:
    """Create the transactions table if needed, and upgrade older versions of it."""
    conn.execute(f"CREATE TABLE IF NOT EXISTS transactions ({COLUMNS})")
    allow_model_source(conn)

def allow_model_source(conn: sqlite3.Connection) -> None:
    """Upgrade an older table so category_source can also be 'model'. Safe to run repeatedly."""
    schema = conn.execute(
        "SELECT sql from sqlite_master WHERE type = 'table' AND name = 'transactions'"
    ).fetchone()[0]
    if "'model'" in schema:
        return
    with conn:
        conn.execute("BEGIN")
        conn.execute(f"CREATE TABLE transactions_new ({COLUMNS})")
        conn.execute("INSERT INTO transactions_new SELECT * FROM transactions")
        conn.execute("DROP TABLE transactions")
        conn.execute("ALTER TABLE transactions_new RENAME TO transactions")

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

def set_manual_category(conn: sqlite3.Connection, transaction_id: int, category: str) -> None:
    """Set a transaction's category by hand and mark it as manual."""
    conn.execute(
        "UPDATE transactions SET category = ?, category_source = 'manual' WHERE id = ?",
        (category, transaction_id)
    )
    conn.commit()

def transactions_to_review(conn: sqlite3.Connection, sample_size: int, seed: int = 0) -> pd.DataFrame:
    """Return transactions to label by hand: all 'other' rows, then a random sample of rule-labelled rows.
    
    Rows already labelled by hand are never included.
    """
    df = load_transactions(conn)
    unreviewed = df[df["category_source"] != "manual"]

    other = unreviewed[unreviewed["category"] == "Other"]
    rule_rows = unreviewed[unreviewed["category"] != "Other"]

    n = min(sample_size, len(rule_rows))
    sample = rule_rows.sample(n=n, random_state=seed)

    return pd.concat([other, sample], ignore_index=True)

def recategorise(conn: sqlite3.Connection) -> None:
    """Re-apply the keyword rules to rule-labelled rows. Manual labels are never changed."""
    rows = conn.execute(
        "SELECT id, description, amount FROM transactions WHERE category_source = 'rule'"
    ).fetchall()
    updates = [(categorise(description, amount), row_id) for row_id, description, amount in rows]
    conn.executemany("UPDATE transactions SET category = ? WHERE id = ?", updates)
    conn.commit()