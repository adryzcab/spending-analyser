import pandas as pd

from spending_analyser.model import load_model, save_model, train_model, predict_confident

def make_training_df():
    """Manual Groceries and Eating out labels, a rare category, and rule rows with a wrong label."""

    rows = (
        [("TESCO STORES", "Groceries", "manual")] * 5
        + [("PRET A MANGER", "Eating out", "manual")] * 5
        + [("EASY JET", "Travel", "manual")] * 2
        + [("TESCO STORES", "Wrong", "rule")] * 5
    )
    return pd.DataFrame(rows, columns=["description", "category", "category_source"])

def test_model_learns_from_manual_labels():
    model = train_model(make_training_df())
    assert list(model.predict(["TESCO STORES", "PRET A MANGER"])) == ["Groceries", "Eating out"]

def test_model_ignores_non_manual_rows():
    model = train_model(make_training_df())
    assert "Wrong" not in model.classes_

def test_model_skips_rare_categories():
    model = train_model(make_training_df())
    assert "Travel" not in model.classes_

def test_saved_model_loads_back(tmp_path):
    model = train_model(make_training_df())
    path = tmp_path / "model.joblib"
    save_model(model, path)
    loaded = load_model(path)
    assert list(loaded.predict(["TESCO EXPRESS"])) == ["Groceries"]

def test_confident_predictions_kept():
    model = train_model(make_training_df())
    result = predict_confident(model, pd.Series(["TESCO STORES"]), threshold=0.5)
    assert result.iloc[0] == "Groceries"

def test_unconfident_predictions_are_none():
    model = train_model(make_training_df())
    result = predict_confident(model, pd.Series(["TESCO STORES"]), threshold=1.01)
    assert result.iloc[0] is None

def rest_predictions_keep_input_index():
    model = train_model(make_training_df())
    descriptions = pd.Series(["TESCO STORES", "PRET A MANGER"], index=[10, 20])
    assert list(result.index) == [10, 20]