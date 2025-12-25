import json
import random
from pathlib import Path

INPUT = Path("data/processed/test.jsonl")
OUTPUT = Path("data/processed/test_noisy.jsonl")

def soften_text(text):
    replacements = {
        "ground delay program": "delays expected",
        "ground stop": "departures temporarily halted",
        "due to": "because of",
        "no significant delays reported": "operations ongoing",
        "weather": "conditions"
    }

    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

def main():
    noisy = []
    with open(INPUT) as f:
        for line in f:
            ex = json.loads(line)
            if random.random() < 0.6:
                ex["text"] = soften_text(ex["text"])
            noisy.append(ex)

    with open(OUTPUT, "w") as f:
        for ex in noisy:
            f.write(json.dumps(ex) + "\n")

    print(f"Created noisy test set: {len(noisy)} examples")

if __name__ == "__main__":
    main()
