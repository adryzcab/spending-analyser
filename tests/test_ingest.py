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

def test_unsorted_files_sorted():
    df = ingest_hsbc_csvs([SAMPLE_PATH_2, SAMPLE_PATH_3, SAMPLE_PATH_1])
    assert len(df) == 13
