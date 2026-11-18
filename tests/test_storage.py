import sqlite3

from spending_analyser.loader import load_hsbc_csv
from spending_analyser.categoriser import add_categories
from spending_analyser.storage import create_table, save_transactions, load_transactions


SAMPLE_PATH = "data/sample/hsbc_sample.csv"




def test_saved_transactions_load_back():
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    df = add_categories(load_hsbc_csv(SAMPLE_PATH))
    save_transactions(df, conn)
    result = load_transactions(conn)
    assert len(result) == 8
