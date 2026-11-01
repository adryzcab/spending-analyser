import pytest

from spending_analyser.analysis import spending_by_category
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