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

