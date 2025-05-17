import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from transformers import BertForSequenceClassification
from sklearn.multioutput import MultiOutputClassifier

def get_bert_model(num_labels=3):
    model = BertForSequenceClassification.from_pretrained(
        'dbmdz/bert-base-turkish-cased', num_labels=num_labels
    )
    return model


class NgramSentimentModel:
    def __init__(self, ngram_range=(1,2), max_features=10000):
        self.vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_features=max_features, lowercase=True)
        self.classifier = MultiOutputClassifier(LogisticRegression(max_iter=1000, random_state=42))
        self.aspect_names = None

    def fit(self, X_train, Y_train):
        X_train_vec = self.vectorizer.fit_transform(X_train)
        self.aspect_names = list(Y_train.columns)
        self.classifier.fit(X_train_vec, Y_train)

    def predict(self, X):
        X_vec = self.vectorizer.transform(X)
        preds = self.classifier.predict(X_vec)
        # Return as DataFrame with aspect columns if aspect_names is set
        import pandas as pd
        if self.aspect_names is not None:
            return pd.DataFrame(preds, columns=self.aspect_names)
        return preds

    def save(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'vectorizer.pkl'), 'wb') as f:
            pickle.dump(self.vectorizer, f)
        with open(os.path.join(output_dir, 'model.pkl'), 'wb') as f:
            pickle.dump(self.classifier, f)
        with open(os.path.join(output_dir, 'aspects.pkl'), 'wb') as f:
            pickle.dump(self.aspect_names, f)

    def load(self, output_dir):
        with open(os.path.join(output_dir, 'vectorizer.pkl'), 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(os.path.join(output_dir, 'model.pkl'), 'rb') as f:
            self.classifier = pickle.load(f)
        aspects_path = os.path.join(output_dir, 'aspects.pkl')
        if os.path.exists(aspects_path):
            with open(aspects_path, 'rb') as f:
                self.aspect_names = pickle.load(f)


def get_ngram_model(ngram_range=(1,1), max_features=2000):
    """
    Returns a new instance of NgramSentimentModel with specified ngram_range and max_features.
    :param ngram_range: Tuple specifying the range of n-grams to consider (default is (1, 1)).
    :param max_features: Maximum number of features to consider (default is 2000).
    :return: An instance of NgramSentimentModel.
    """
    return NgramSentimentModel(ngram_range=ngram_range, max_features=max_features)