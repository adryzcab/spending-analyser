import pytest
import pandas as pd

from spending_analyser.analysis import spending_by_category, monthly_spending, monthly_change
from spending_analyser.categoriser import add_categories
from spending_analyser.loader import load_hsbc_csv

SAMPLE_PATH = "data/sample/hsbc_sample.csv"


def get_category_totals():
    """Load the sample data and return spending per category"""
    df = load_hsbc_csv(SAMPLE_PATH)
    df = add_categories(df)
    return spending_by_category(df)

def test_income_excluded():
    result = get_category_totals()
    assert "Income" not in result.index

def test_totals_are_positive():
    result = get_category_totals()
    assert (result > 0).all()

def test_largest_category_first():
    result = get_category_totals()
    assert result.index[0] == "Rent"

def test_eating_out_total_summed():
    result = get_category_totals()
    assert result["Eating out"] == pytest.approx(10.65)


def test_same_month_summed():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-15"]),
        "amount": [-10.0, -5.0]
    })
    result = monthly_spending(df)
    assert len(result) == 1
    assert result.iloc[0] == 15

def test_monthly_income_excluded():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-15"]),
        "amount": [-10.0, 14.0]
    })
    result = monthly_spending(df)
    assert result.iloc[0] == 10.0

def test_same_month_different_years():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2020-10-01", "2026-10-15"]),
        "amount": [-10.0, -5.0]
    })
    result = monthly_spending(df)
    assert len(result) == 2
    assert result.iloc[0] == 10

def test_monthly_change_values():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-08-01", "2026-09-01", "2026-10-01"]),
        "amount": [-300.0, -450.0, -400.0],
    })
    result = monthly_change(df)
    assert result.iloc[1] == 150
    assert result.iloc[2] == -50

def test_montly_change_first_month_nan():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-08-01", "2026-09-01"]),
        "amount": [-300.0, -450.0]
    })
    result = monthly_change(df)
    assert pd.isna(result.iloc[0])