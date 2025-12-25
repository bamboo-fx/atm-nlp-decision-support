import json
import random
from datetime import timedelta

AIRPORTS = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SFO"]
CAUSES = ["weather", "thunderstorms", "low visibility", "runway maintenance", "staffing"]
DELAYS = [30, 45, 60, 90, 120]

TEMPLATES = {
    "GDP": "GROUND DELAY PROGRAM IN EFFECT FOR {airport} DUE TO {cause}. EXPECTED DELAYS UP TO {delay} MINUTES UNTIL {end_time}.",
    "GS": "GROUND STOP IN EFFECT FOR {airport} DUE TO {cause}. NO DEPARTURES AUTHORIZED UNTIL {end_time}.",
    "REROUTE": "TRAFFIC FROM {origin} TO {destination} MUST REROUTE DUE TO {cause}.",
    "WX": "WEATHER ADVISORY FOR {airport}. OPERATIONS IMPACTED DUE TO {cause}.",
    "CAPACITY": "RUNWAY CONFIGURATION CHANGE AT {airport} DUE TO {cause}. EXPECT LIMITED CAPACITY.",
    "NORMAL": "NORMAL OPERATIONS RESUMED AT {airport}. NO SIGNIFICANT DELAYS REPORTED."
}

def random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02d}{minute: 02d}Z"

def generate_example(label, idx):
    airport = random.choice(AIRPORTS)
    cause = random.choice(CAUSES)
    end_time = random_time()
    delay = random.choice(DELAYS)

    if label == "REROUTE":
        origin, destination = random.sample(AIRPORTS, 2)
        text = TEMPLATES[label].format(
            origin=origin,
            destination=destination,
            cause=cause
        )
        airports = [origin, destination]
    else:
        text = TEMPLATES[label].format(
            airport=airport,
            cause=cause,
            delay=delay,
            end_time=end_time
        )
        airports = [airport]

    return {
        "id": f"ADV_{idx:04d}",
        "text": text,
        "label": label,
        "metadata": {
            "airports": airports,
            "cause": cause,
            "end_time": end_time
        }
    }

def main(n_examples=300):
    labels = list(TEMPLATES.keys())
    data = []

    for i in range(n_examples):
        label = random.choice(labels)
        example = generate_example(label, i)
        data.append(example)

    with open("data/raw/advisories.jsonl", "w") as f:
        for ex in data:
            f.write(json.dumps(ex) + "\n")

    print(f"Generated {len(data)} synthetic advisories.")

if __name__ == "__main__":
    main()
