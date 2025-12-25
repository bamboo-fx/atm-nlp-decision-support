import json
from pathlib import Path
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

DATA_DIR = Path("data/processed")

def load_split(filename):
    texts, labels = [], []
    with open(DATA_DIR / filename) as f:
        for line in f:
            ex = json.loads(line)
            texts.append(ex["text"])
            labels.append(ex["label"])
    return texts, labels

def main():
    train_texts, train_labels = load_split("train.jsonl")
    test_texts, test_labels = load_split("test.jsonl")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    X_train = embedder.encode(train_texts)
    X_test = embedder.encode(test_texts)

    le = LabelEncoder()
    y_train = le.fit_transform(train_labels)
    y_test = le.transform(test_labels)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)

    probs = clf.predict_proba(X_test)
    preds = clf.predict(X_test)

    confidences = probs.max(axis=1)
    sorted_idx = np.argsort(confidences)

    print("Lowest-confidence predictions:\n")
    for i in sorted_idx[:5]:
        print(f"Text: {test_texts[i]}")
        print(f"True: {test_labels[i]}")
        print(f"Pred: {le.inverse_transform([preds[i]])[0]}")
        print(f"Confidence: {confidences[i]:.3f}")
        print("-" * 50)

if __name__ == "__main__":
    main()
