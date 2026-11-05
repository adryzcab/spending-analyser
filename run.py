import sys

from spending_analyser.loader import load_hsbc_csv
from spending_analyser.analysis import monthly_summary


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <path-to-your-csv>")
        sys.exit(1)
    csv_path = sys.argv[1]
    df = load_hsbc_csv(csv_path)
    print(monthly_summary(df))


if __name__ == "__main__":
    main()
