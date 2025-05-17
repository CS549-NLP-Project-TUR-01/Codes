import pandas as pd
from models.instances import get_ngram_model
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os

# Save results
import json


def evaluate_bert_model(true_labels, predictions, label_names):
    report = classification_report(true_labels, predictions, target_names=label_names)
    accuracy = accuracy_score(true_labels, predictions)
    return report, accuracy


def evaluate_ngram_model(val_df, output_dir, aspect_cols=None):
    model = get_ngram_model()
    model.load(output_dir)
    X_val = val_df['review_text'].astype(str)
    
    if aspect_cols is None:
        aspect_cols = [col for col in val_df.columns if col not in ['review_text']]
    Y_val = val_df[aspect_cols]
    Y_pred = model.predict(X_val)
    results = {}
    for aspect in aspect_cols:
        y_true = Y_val[aspect]
        y_pred = Y_pred[aspect]
        acc = accuracy_score(y_true, y_pred)
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_true, y_pred)
        results[aspect] = {
            'accuracy': acc,
            'classification_report': report,
            'confusion_matrix': cm.tolist()
        }

    with open(os.path.join(output_dir, 'results.json'), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    return results
