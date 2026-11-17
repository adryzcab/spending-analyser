# Spending Analyser

A Python tool that analyses, categorises, and visualises personal spending to take the guesswork out of budgeting.

## Motivation
I'm not the type to track my expenses. I do everything in my head, rounding up, estimating, and simply hoping my budget is still on track.
This project helps me see exactly where my money goes and how much I spend each month.

## Setup
Requires Python 3.11.

```
python -m venv .venv
```

Activate the virtual environment:

- Windows: `.venv\Scripts\activate`
- Mac/Linux: `source .venv/bin/activate`

Then install:

```
pip install -e .
pip install pytest
```

Run the tests with:

```
pytest
```

## Planned Features
- [x] Load and clean bank transaction CSV
- [x] Categorise transactions
- [x] Analyse and visualise spending
- [x] Combine multiple CSVs with de-duplication
- [ ] Automatically ingest new CSVs
- [ ] Interactive dashboard
- [ ] ML-based auto-categorisation

## Tech Stack
Python, pandas, matplotlib, pytest

## Status
🚧 In progress