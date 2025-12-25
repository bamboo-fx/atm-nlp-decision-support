import json
import random
from pathlib import Path

RAW_DATA_PATH = Path("data/raw/advisories.jsonl")
PROCESSED_DIR = Path("data/processed")

TRAIN_RATIO = 0.7
VAL_RATIO = 0.15
TEST_RATIO = 0.15

def clean_text(text: str) -> str:
    """
    Light text normalization.
    We intentionally keep most structure intact for sentence embeddings.
    """
    text = text.strip()
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text.lower()

def load_data():
    examples = []
    with open(RAW_DATA_PATH, "r") as f:
        for line in f:
            examples.append(json.loads(line))
    return examples

def split_data(examples):
    random.shuffle(examples)
    n = len(examples)

    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)

    train = examples[:train_end]
    val = examples[train_end:val_end]
    test = examples[val_end:]

    return train, val, test

def save_split(split, filename):
    with open(PROCESSED_DIR / filename, "w") as f:
        for ex in split:
            record = {
                "id": ex["id"],
                "text": clean_text(ex["text"]),
                "label": ex["label"]
            }
            f.write(json.dumps(record) + "\n")

def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    examples = load_data()
    train, val, test = split_data(examples)

    save_split(train, "train.jsonl")
    save_split(val, "val.jsonl")
    save_split(test, "test.jsonl")

    print(f"Total examples: {len(examples)}")
    print(f"Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")

if __name__ == "__main__":
    main()
