import matplotlib.pyplot as plt
import pandas as pd

from spending_analyser.analysis import spending_by_category, monthly_change, monthly_summary

def plot_spending_by_category(df: pd.DataFrame):
    """Return a bar chart of spending by category"""
    data = spending_by_category(df)
    ax = data.plot(kind="bar", rot=0)
    ax.set_title("Spending by category")
    ax.set_ylabel("£ spent")
    return ax

def plot_monthly_change(df: pd.DataFrame):
    """Return a line chart of spending change vs the previous month."""
    data = monthly_change(df)
    ax = data.plot(kind="line", marker="o")
    ax.axhline(0, color="grey", linewidth=1)
    ax.set_title("Change in spending vs the previous month")
    ax.set_ylabel("£ change")
    return ax

def plot_monthly_summary(df: pd.DataFrame):
    """Return a grouped bar chart of income vs spending per month."""
    data = monthly_summary(df)
    ax = data[["income", "spending"]].plot(kind="bar", rot=0)
    ax.set_title("Income vs spending per month")
    ax.set_ylabel("£")
    return ax