import sqlite3
import pandas as pd

from spending_analyser.loader import load_hsbc_csv
from spending_analyser.categoriser import add_categories
from spending_analyser.storage import create_table, save_transactions, load_transactions, set_manual_category, transactions_to_review, recategorise


SAMPLE_PATH = "data/sample/hsbc_sample.csv"

def make_saved_db():
    """Return a connection to an in-memory database with the sample data saved."""
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = add_categories(load_hsbc_csv(SAMPLE_PATH))
    save_transactions(df, conn)
    return conn


def test_saved_transactions_load_back():
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = add_categories(load_hsbc_csv(SAMPLE_PATH))
    save_transactions(df, conn)
    result = load_transactions(conn)
    assert len(result) == 8

def test_dates_load_back_as_dates():
    result = load_transactions(make_saved_db())
    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert result["date"].notna().all()

def test_saved_rows_marked_as_rule():
    result = load_transactions(make_saved_db())
    assert (result["category_source"] == "rule").all()

def test_save_does_not_change_input():
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = add_categories(load_hsbc_csv(SAMPLE_PATH))
    save_transactions(df, conn)
    assert pd.api.types.is_datetime64_any_dtype(df["date"])

def test_manual_category_is_saved():
    conn = make_saved_db()
    set_manual_category(conn, 1, "Work expense")
    result = load_transactions(conn)
    row = result[result["id"] == 1]
    assert row["category"].iloc[0] == "Work expense"
    assert row["category_source"].iloc[0] == "manual"

def test_manual_category_changes_only_one_row():
    conn = make_saved_db()
    set_manual_category(conn, 1, "Work expense")
    result = load_transactions(conn)
    assert (result["category_source"] == "manual").sum() == 1

def make_review_db():
    """A database with 2 'Other' rows and 5 rule-labelled rows."""
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01"] * 7),
        "description": ["SHOP A", "SHOP B", "TESCO", "TESCO", "PRET A MANGER", "TFL TRAVEL CH", "UBER *TRIP"],
        "amount": [-5.0] * 7,
        "category": ["Other", "Other", "Groceries", "Groceries", "Eating out", "Transport", "Transport"],
    })
    save_transactions(df, conn)
    return conn

def test_review_includes_all_other_rows():
    result = transactions_to_review(make_review_db(), sample_size=2)
    assert (result["category"] == "Other").sum() == 2

def test_review_sample_size():
    result = transactions_to_review(make_review_db(), sample_size=2)
    assert len(result) == 4

def test_review_skips_manual_rows():
    conn = make_review_db()
    set_manual_category(conn, 1, "Gifts")
    result = transactions_to_review(conn, sample_size=10)
    assert 1 not in result["id"].values

def test_review_sample_is_reproducible():
    first = transactions_to_review(make_review_db(), sample_size=2, seed=42)
    second = transactions_to_review(make_review_db(), sample_size=2, seed=42)
    assert list(first["id"]) == list(second["id"])

def make_outdates_db():
    """Two TESCO rows saved with an outdated category; row 2 is then labelled by hand."""
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-02"]),
        "description": ["TESCO STORES", "TESCO STORES"],
        "amount": [-10.0, -20.0],
        "category": ["Other", "Other"],
    })
    save_transactions(df, conn)
    set_manual_category(conn, 2, "Gifts")
    return conn

def test_recategorise_updates_rule_rows():
    conn = make_outdates_db()
    recategorise(conn)
    result = load_transactions(conn)
    assert result[result["id"] == 1]["category"].iloc[0] == "Groceries"

def test_recategorise_keeps_manual_labels():
    conn = make_outdates_db()
    recategorise(conn)
    result = load_transactions(conn)
    assert result[result["id"] == 2]["category"].iloc[0] == "Gifts" 

OLD_COLUMNS = """
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT,
    category_source TEXT CHECK (category_source IN ('rule', 'manual'))
"""

def make_old_db():
    """A database created with the old table rule, holding one manual label."""
    conn = sqlite3.connect(":memory:")
    conn.execute(f"CREATE TABLE transactions ({OLD_COLUMNS})")
    conn.execute(
        "INSERT INTO transactions (date, description, amount, category, category_source) "
        "VALUES ('2026-10-01', 'TESCO STORES', -10.0, 'Gifts', 'manual')"
    )
    conn.commit()
    return conn

def test_upgrade_keeps_existing_rows():
    conn = make_old_db()
    create_table(conn)
    result = load_transactions(conn)
    assert len(result) == 1
    assert result["category"].iloc[0] == "Gifts"

def test_upgrade_allows_model_sources():
    conn = make_old_db()
    create_table(conn)
    conn.execute("UPDATE transactions SET category_source = 'model' WHERE id = 1")

def test_upgrade_is_safe_to_repeat():
    conn = make_old_db()
    create_table(conn)
    create_table(conn)
    assert len(load_transactions(conn)) == 1