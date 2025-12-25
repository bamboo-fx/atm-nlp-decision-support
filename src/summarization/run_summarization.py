import json
from pathlib import Path
from .generate_summary import generate_summary

INPUT = Path("data/processed/test_extracted.jsonl")
OUTPUT = Path("data/processed/test_summarized.jsonl")

def main():
    with open(INPUT) as f, open(OUTPUT, "w") as out:
        for line in f:
            ex = json.loads(line)
            summary = generate_summary(
                label=ex["label"],
                extracted=ex["extracted"]
            )
            ex["summary"] = summary
            out.write(json.dumps(ex) + "\n")

    print("Summarization complete.")

if __name__ == "__main__":
    main()
