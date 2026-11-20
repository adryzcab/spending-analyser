from spending_analyser.labelling import resolve_answer

CATEGORIES = ["Eating out", "Groceries", "Shopping"]

def test_empty_answer_keeps_current():
    assert resolve_answer("", "Groceries", CATEGORIES) == "Groceries"

def test_asnwer_ignores_case_and_spaces():
    assert resolve_answer("  eating OUT", "Other", CATEGORIES) == "Eating out"

def test_unknown_answer_returns_none():
    assert resolve_answer("Holidays", "Other", CATEGORIES) is None