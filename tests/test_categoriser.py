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

def test_outgoing_wise_is_transfer():
    assert categorise("WISE", -200.00) == "Transfer"

def test_incoming_wise_is_transfer():
    assert categorise("WISE", 150.00) == "Transfer"

def test_other_positive_amount_still_income():
    assert categorise("SALARY ACME LTD", 1850.00) == "Income"

def test_bank_fee_is_fees():
    assert categorise("NON-STERLING TRANSACTION FEE", -0.43) == "Fees"

def test_lidl_is_groceries():
    assert categorise("LIDL GB LONDON", -23.10) == "Groceries"

def test_iceland_is_groceries():
    assert categorise("ICELAND STEPNEY", -9.75) == "Groceries"

def test_gym_is_subscriptions():
    assert categorise("PUREGYM", -22.0) == "Subscriptions"

def test_eonnext_is_utility():
    assert categorise("E.ON NEXT", -22.0) == "Utilities"

def test_octopus_is_utility():
    assert categorise("OCTOPUS", -22.0) == "Utilities"

def test_communityfibre_is_utility():
    assert categorise("COMMUNITYFIBRE", -22.0) == "Utilities"

def test_primark_is_shopping():
    assert categorise("PRIMARK", -23.4) == "Shopping"

def test_temu_is_shopping():
    assert categorise("TEMU.COM", -23.6) == "Shopping"

def test_supermarket_is_groceries():
    assert categorise("WATNEY SUPERMARKET", -12.1) == "Groceries"

def test_tiantian_is_groceries():
    assert categorise("TIAN TIAN MARKET", -3.52) == "Groceries"

def test_aldi_is_groceries():
    assert categorise("ALDI LONDON", -7.32) == "Groceries"

def test_oseyo_is_groceries():
    assert categorise("OSEYO LONDON", -9.13) == "Groceries"
