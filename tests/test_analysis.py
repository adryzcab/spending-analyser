import pytest
import pandas as pd

from spending_analyser.analysis import spending_by_category, monthly_spending, monthly_change, monthly_income, monthly_summary, unusual_transactions
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

def test_monthly_income_excludes_spending():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-15", "2026-10-20"]),
        "amount": [1000.0, 200.0, -300.0],
    })
    result = monthly_income(df)
    assert len(result) == 1
    assert result.iloc[0] == 1200.0

def test_monthly_income_month_without_income():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-11-05"]),
        "amount": [1000.0, -300.0],
    })
    result = monthly_income(df)
    assert len(result) == 1

def test_monthly_summary_net():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-05", "2026-10-20"]),
        "amount": [1000.0, -200.0, -300.0],
    })
    result = monthly_summary(df)
    assert result["net"].iloc[0] == 500.0

def test_monthly_summary_missing_income_is_zero():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-11-05"]),
        "amount": [1000.0, -300.0]
    })
    result = monthly_summary(df)
    assert result["income"].iloc[1] == 0
    assert result["net"].iloc[1] == -300

def test_monthly_summary_empty_input():
    df = pd.DataFrame({
        "date": pd.to_datetime([]),
        "amount": pd.Series([], dtype=float),
    })
    result = monthly_summary(df)
    assert len(result) == 0

def make_unusual_df():
    """Shopping with one big purchase, identical rent payments, and income."""
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01"] * 9),
        "amount": [-10.0, -11.0, -12.0, -13.0, -100.0, -1150.0, -1150.0, -1150.0, 2000.0,],
        "category": ["Shopping"] * 5 + ["Rent"] * 3 + ["Income"],
    })

def test_unusual_purchase_flagged():
    result = unusual_transactions(make_unusual_df())
    assert len(result) == 1
    assert result["amount"].iloc[0] == -100.0

def test_identical_amounts_not_flagged():
    result = unusual_transactions(make_unusual_df())
    assert "Rent" not in result["category"].values

def test_income_ignored():
    result = unusual_transactions(make_unusual_df())
    assert (result["amount"] < 0).all()

def make_transfer_df():
    """One month: salary, a purchase, and a transfer both ways"""
    return pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04"]),
        "description": ["SALARY ACME LTD", "TESCO STORES", "WISE", "WISE"],
        "amount": [1000.0, -50.0, -200.0, 100.0],
        "category": ["Income", "Groceries", "Transfer", "Transfer"],
    })

def test_transfers_not_counted_as_spending():
    summary = monthly_summary(make_transfer_df())
    assert summary["spending"].iloc[0] == 50.0

def test_transfers_not_counted_as_income():
    summary = monthly_summary(make_transfer_df())
    assert summary["income"].iloc[0] == 1000.0

def test_transfers_not_in_spending_by_category():
    result = spending_by_category(make_transfer_df())
    assert "Transfer" not in result.index