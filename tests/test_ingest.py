import pandas as pd

from spending_analyser.ingest import ingest_hsbc_csvs

SAMPLE_PATH_1 = "data/sample/hsbc_overlap_1.csv"
SAMPLE_PATH_2 = "data/sample/hsbc_overlap_2.csv"
SAMPLE_PATH_3 = "data/sample/hsbc_overlap_3.csv"


def test_overlapping_days_not_double_counted():
    df = ingest_hsbc_csvs([SAMPLE_PATH_1, SAMPLE_PATH_2])
    assert len(df) == 10

def test_identical_transactions_not_miscounted():
    df = ingest_hsbc_csvs([SAMPLE_PATH_1, SAMPLE_PATH_2])
    pret = df[(df["description"] == "PRET A MANGER") & (df["date"] == pd.Timestamp("2026-10-29"))]
    assert len(pret) == 2


def test_incomplete_day_transactions_included():
    df = ingest_hsbc_csvs([SAMPLE_PATH_1, SAMPLE_PATH_2])
    nandos = df[df["description"] == "NANDOS"]
    assert len(nandos) == 1

def test_3_samples_have_13_rows():
    df = ingest_hsbc_csvs([SAMPLE_PATH_1, SAMPLE_PATH_2, SAMPLE_PATH_3])
    assert len(df) == 13

def test_pret_3_NOV_included():
    df = ingest_hsbc_csvs([SAMPLE_PATH_1, SAMPLE_PATH_2, SAMPLE_PATH_3])
    pret = df[(df["description"] == "PRET A MANGER")]
    assert len(pret) == 3

def test_file_order_does_not_matter():
    df = ingest_hsbc_csvs([SAMPLE_PATH_2, SAMPLE_PATH_3, SAMPLE_PATH_1])
    assert len(df) == 13


import sqlite3

import pytest

from spending_analyser.ingest import add_statement, add_statements
from spending_analyser.storage import create_table, load_transactions

def make_empty_db():
    """Return a connection to an empty in-memory database."""
    conn = sqlite3.connect(":memory:")
    create_table(conn)
    return conn

def test_first_statement_skips_last_day():
    conn = make_empty_db()
    add_statement(SAMPLE_PATH_1, conn)
    assert len(load_transactions(conn)) == 6

def test_overlapping_between_statements_not_duplicated():
    conn = make_empty_db()
    add_statement(SAMPLE_PATH_1, conn)
    add_statement(SAMPLE_PATH_2, conn)
    add_statement(SAMPLE_PATH_3, conn)
    assert len(load_transactions(conn)) == 12

def test_gap_between_statements_raises_error():
    conn = make_empty_db()
    add_statement(SAMPLE_PATH_1, conn)
    with pytest.raises(ValueError):
        add_statement(SAMPLE_PATH_3, conn)

def test_same_statement_twice_not_duplicated():
    conn = make_empty_db()
    add_statement(SAMPLE_PATH_1, conn)
    add_statement(SAMPLE_PATH_1, conn)
    assert len(load_transactions(conn)) == 6

def test_statement_order_does_not_matter():
    conn = make_empty_db()
    add_statements([SAMPLE_PATH_1, SAMPLE_PATH_2, SAMPLE_PATH_3], conn)
    assert len(load_transactions(conn)) == 12
