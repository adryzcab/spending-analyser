import sys

from spending_analyser.ingest import ingest_hsbc_csvs
from spending_analyser.analysis import monthly_summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <csv> [<csv> ...]")
        sys.exit(1)
    csv_paths = sys.argv[1:]
    df = ingest_hsbc_csvs(csv_paths)
    print(monthly_summary(df))


if __name__ == "__main__":
    main()
