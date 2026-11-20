import sys
import sqlite3

from spending_analyser.ingest import add_statements
from spending_analyser.analysis import monthly_summary
from spending_analyser.storage import create_table, load_transactions, recategorise

DB_PATH = "data/spending.db"



def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <csv> [<csv> ...]")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    for path in sys.argv[1:]:
        add_statements(path, conn)
        recategorise(conn)
    print(monthly_summary(load_transactions(conn)))
    conn.close()



if __name__ == "__main__":
    main()
