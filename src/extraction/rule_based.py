import json
import re
from pathlib import Path

DATA_DIR = Path("data/processed")

AIRPORT_PATTERN = re.compile(r"\b[A-Z]{3}\b")
TIME_PATTERN = re.compile(r"\b\d{2}\s?\d{2}Z\b|\b\d{4}Z\b")

CAUSE_KEYWORDS = {
    "weather": ["weather", "thunderstorm", "low visibility", "conditions"],
    "runway_maintenance": ["runway maintenance", "runway"],
    "staffing": ["staffing"],
}

def extract_airports(text):
    return list(set(AIRPORT_PATTERN.findall(text.upper())))

def extract_end_time(text):
    match = TIME_PATTERN.search(text.upper())
    return match.group(0).replace(" ", "") if match else None

def extract_cause(text):
    t = text.lower()
    for cause, keywords in CAUSE_KEYWORDS.items():
        for kw in keywords:
            if kw in t:
                return cause
    return "unknown"

def process_file(input_file, output_file):
    with open(DATA_DIR / input_file) as f, open(DATA_DIR / output_file, "w") as out:
        for line in f:
            ex = json.loads(line)
            text = ex["text"]

            extracted = {
                "id": ex["id"],
                "text": text,
                "label": ex["label"],
                "extracted": {
                    "airports": extract_airports(text),
                    "end_time": extract_end_time(text),
                    "cause": extract_cause(text),
                }
            }
            out.write(json.dumps(extracted) + "\n")

def main():
    process_file("test.jsonl", "test_extracted.jsonl")
    print("Extraction complete.")

if __name__ == "__main__":
    main()
