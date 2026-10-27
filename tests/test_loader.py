import pandas as pd
from spending_analyser.loader import load_hsbc_csv


SAMPLE_PATH = "data/sample/hsbc_sample.csv"


def test_load_all_rows():
    df = load_hsbc_csv(SAMPLE_PATH)
    assert len(df) == 8

def test_amount_is_float():
    df = load_hsbc_csv(SAMPLE_PATH)
    assert pd.api.types.is_float_dtype(df["amount"])


def test_date_is_datetime():
    df = load_hsbc_csv(SAMPLE_PATH)
    assert pd.api.types.is_datetime64_any_dtype(df["date"])


def test_first_date_parsed_day_first():
    df = load_hsbc_csv(SAMPLE_PATH)
    assert df["date"].iloc[0] == pd.Timestamp("2026-10-01")


def test_thousands_amount_parsed():
    df = load_hsbc_csv(SAMPLE_PATH)
    assert df["amount"].iloc[5] == -1200.0
