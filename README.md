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

## Usage
Run `run.py` with one or more HSBC CSV exports, **oldest first**.
Transactions are saved to a local SQLite database (`data/spending.db`),
and a monthly summary of income, spending and net is printed for
everything stored so far.

```
python run.py <csv> [<csv> ...]
```

Each month, run it with just your new statement:

```
python run.py data/sample/hsbc_overlap_2.csv
```

Notes:
- Each statement must overlap the previous one by at least one day,
  otherwise it's rejected to avoid missing transactions.
- A statement's last day is held back (it may be incomplete) and is
  added from the next statement.
- Adding the same statement twice has no effect.
- The database file is git-ignored, so your bank data is never committed.

## Planned Features
- [x] Load and clean bank transaction CSV
- [x] Categorise transactions
- [x] Analyse and visualise spending
- [x] Combine multiple CSVs with de-duplication
- [x] Store transactions in SQLite, with manual category corrections
- [x] Add new statements to the database without duplicates
- [ ] Automatically ingest new CSVs from a folder
- [ ] Interactive dashboard
- [ ] ML-based auto-categorisation

## Tech Stack
Python, pandas, matplotlib, SQLite, pytest

## Status
🚧 In progress