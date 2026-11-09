from spending_analyser.categoriser import categorise, add_categories
from spending_analyser.loader import load_hsbc_csv

SAMPLE_PATH = "data/sample/hsbc_sample.csv"

# categorise(): single transaction

def test_tesco_is_groceries():
    assert categorise("TESCO STORES 3927 LONDON", -14.62) == 'Groceries'

def test_lowercase_description_still_matches():
    assert categorise("tesco express", -3.10) == "Groceries"

def test_keyword_at_end_matches():
    assert categorise("QUEENS COURT RENT", -1200.00) == "Rent"

def test_positive_amount_is_income():
    assert categorise("STUDENT LOAN COMPANY", 1850.00) == "Income"

def test_positive_amount_beats_keyword():
    assert categorise("TESCO REFUND", 5.00) == "Income"

def test_unknown_description_is_other():
    assert categorise("RANDOM SHOP", -5.00) == "Other"

def test_netflix_is_subscriptions():
    assert categorise("NETFLIX.COM", -10.99) == "Subscriptions"

def test_boots_is_self_care():
    assert categorise("BOOTS", -7.43) == "Self care"

def test_steam_is_entertainment():
    assert categorise("STEAM GAMES", -32.00) == "Entertainment"

def test_nandos_is_eating_out():
    assert categorise("NANDOS", -23.42) == "Eating out"

def test_spotify_is_subscriptions():
    assert categorise("SPOTIFY", -7.00) == "Subscriptions"

def test_sainsburys_is_groceries():
    assert categorise("SAINSBURYS", -43.57) == "Groceries"

    



# add_categories(): Whole DataFrame

def test_add_categories_creates_column():
    df = load_hsbc_csv(SAMPLE_PATH)
    result = add_categories(df)
    assert result["category"].iloc[5] == "Rent"