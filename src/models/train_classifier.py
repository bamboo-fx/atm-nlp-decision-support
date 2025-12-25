import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_DIR = Path("data/processed")
MODEL_DIR = Path("models")

def load_split(filename):
    texts = []
    labels = []
    with open(DATA_DIR / filename, "r") as f:
        for line in f:
            ex = json.loads(line)
            texts.append(ex["text"])
            labels.append(ex["label"])
    return texts, labels

def main():
    MODEL_DIR.mkdir(exist_ok=True)

    # Load data
    train_texts, train_labels = load_split("train.jsonl")
    val_texts, val_labels = load_split("val.jsonl")
    test_texts, test_labels = load_split("test.jsonl")

    # Load sentence embedding model
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed text
    X_train = embedder.encode(train_texts, show_progress_bar=True)
    X_val = embedder.encode(val_texts, show_progress_bar=True)
    X_test = embedder.encode(test_texts, show_progress_bar=True)

    # Train classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, train_labels)

    # Evaluate
    val_preds = clf.predict(X_val)
    test_preds = clf.predict(X_test)

    print("Validation Accuracy:", accuracy_score(val_labels, val_preds))
    print("Test Accuracy:", accuracy_score(test_labels, test_preds))
    print("\nClassification Report (Test):")
    print(classification_report(test_labels, test_preds))

    print("\nConfusion Matrix (Test):")
    print(confusion_matrix(test_labels, test_preds))

if __name__ == "__main__":
    main()
