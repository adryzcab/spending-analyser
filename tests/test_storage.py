import sqlite3
import pandas as pd

from spending_analyser.loader import load_hsbc_csv
from spending_analyser.categoriser import add_categories
from spending_analyser.storage import create_table, save_transactions, load_transactions, set_manual_category


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


