import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

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
    noisy_texts, noisy_labels = load_split("test_noisy.jsonl")

    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    X_train = embedder.encode(train_texts)
    X_noisy = embedder.encode(noisy_texts)

    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, train_labels)

    preds = clf.predict(X_noisy)

    print("Noisy Test Classification Report:\n")
    print(classification_report(noisy_labels, preds))

if __name__ == "__main__":
    main()
