import sqlite3

from spending_analyser.categoriser import CATEGORY_RULES
from spending_analyser.labelling import resolve_answer
from spending_analyser.storage import create_table, set_manual_category, transactions_to_review

DB_PATH = "data/spending.db"
CATEGORIES = sorted(list(CATEGORY_RULES)) + ["Other", "Income"]


def main():
    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
    rows = transactions_to_review(conn, sample_size=20)

    print("Categories:", ", ".join(CATEGORIES))
    print("Enter = keep, s = skip, q = quit\n")

    for _, row in rows.iterrows():
        print(f"{row['date']:%Y-%m-%d} {row['description']} ${row['amount']:.2f} [{row['category']}]")
        while True:
            answer = input("> ")
            if answer == "q":
                conn.close()
                return
            if answer == "s":
                break
            category = resolve_answer(answer, row["category"], CATEGORIES)
            if category is None:
                print("Unknown category, try again.")
                continue
            set_manual_category(conn, int(row["id"]), category)
            break

    conn.close()
    print("Done.")


if __name__ == "__main__":
    main()