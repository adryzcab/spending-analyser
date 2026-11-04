import pandas as pd

from spending_analyser.plots import plot_spending_by_category, plot_monthly_change, plot_monthly_summary



def test_plot_spending_by_category():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-05"]),
        "amount": [-20.0, -10.0],
        "category": ["Groceries", "Transport"],
    })
    ax = plot_spending_by_category(df)
    assert ax.get_title() == "Spending by category"

def test_plot_monthly_change_title():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-09-01", "2026-10-01"]),
        "amount": [-100.0, -150.0],
    })
    ax = plot_monthly_change(df)
    assert ax.get_title() == "Change in spending vs the previous month"

def test_plot_monthly_summary_title():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-10-01", "2026-10-15"]),
        "amount": [1000.0, -200.0]
    })
    ax = plot_monthly_summary(df)
    assert ax.get_title() == "Income vs spending per month"