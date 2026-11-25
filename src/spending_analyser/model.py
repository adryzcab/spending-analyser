import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, make_pipeline

MIN_EXAMPLES = 5

def train_model(df: pd.DataFrame) -> Pipeline:
    """Train a category model on manually labelled transactions only.
    
    
    Categories with fewer than MIN_EXAMPLES labels are left out
    because the models can't learn a category from so few examples.
    """
    labelled = df[df["category_source"] == "manual"]
    counts = labelled["category"].value_counts()
    keep = counts[counts >= MIN_EXAMPLES].index
    labelled = labelled[labelled["category"].isin(keep)]

    pipeline = make_pipeline(CountVectorizer(), MultinomialNB())
    pipeline.fit(labelled["description"], labelled["category"])
    return pipeline


def save_model(pipeline: Pipeline, path: str) -> None:
    """Saves a trained model to a file."""
    joblib.dump(pipeline, path)


def load_model(path: str) -> Pipeline:
    """Load a model saved with save_model."""
    return joblib.load(path)

def predict_confident(model: Pipeline, description: pd.Series, threshold: float) -> pd.Series:
    """Predict categories, keeping only predictions at least 'threshold confident'.
    
    Less confident predictions are returned as None.
    """
    probabilities = model.predict_proba(description)
    best = probabilities.argmax(axis=1)
    confidence = probabilities.max(axis=1)

    result = pd.Series(model.classes_[best], index=descriptions.index, dtype=object)
    result[confidence < threshold] = None
    return result