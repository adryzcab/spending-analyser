import pandas as pd

from spending_analyser.ingest import ingest_hsbc_csvs

SAMPLE_PATH_1 = "data/sample/hsbc_overlap_1.csv"
SAMPLE_PATH_2 = "data/sample/hsbc_overlap_2.csv"


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
